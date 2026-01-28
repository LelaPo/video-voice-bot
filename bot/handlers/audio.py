import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.config import config
from bot.services.converter import ConversionService
from bot.utils.temp_file import TempFileManager
from bot.utils.media_detect import is_audio_file, is_video_file, get_extension
from bot.states import UserState

router = Router()
semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
converter = ConversionService()


async def process_audio_to_voice(message: Message, bot: Bot, file_id: str, file_size: int, filename: str | None):
    if file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю аудио...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = get_extension(filename, ".mp3")
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".ogg")
            
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, input_path)
            
            await status_message.edit_text("Конвертирую в голосовое...")
            
            result = await converter.convert_to_voice(input_path, output_path)
            
            if not result.success:
                await status_message.edit_text(f"Ошибка конвертации: {result.error}")
                return
            
            await status_message.edit_text("Отправляю голосовое сообщение...")
            
            voice_file = FSInputFile(output_path)
            await message.reply_voice(
                voice=voice_file,
                duration=result.duration
            )
            
            await status_message.edit_text("Готово!")
            
        except Exception as e:
            await status_message.edit_text(f"Произошла ошибка: {str(e)}")
        
        finally:
            temp_manager.cleanup(input_path)
            temp_manager.cleanup(output_path)


@router.message(F.audio, UserState.audio_to_voice)
async def handle_audio_voice_mode(message: Message, bot: Bot):
    audio = message.audio
    await process_audio_to_voice(message, bot, audio.file_id, audio.file_size, audio.file_name)


@router.message(F.audio)
async def handle_audio_auto(message: Message, bot: Bot):
    audio = message.audio
    await process_audio_to_voice(message, bot, audio.file_id, audio.file_size, audio.file_name)


@router.message(F.document, UserState.audio_to_voice)
async def handle_document_voice_mode(message: Message, bot: Bot):
    document = message.document
    if not is_audio_file(document.file_name, document.mime_type):
        await message.reply(
            "Это не аудиофайл.\n"
            "Поддерживаемые форматы: mp3, wav, m4a, ogg, flac"
        )
        return
    await process_audio_to_voice(message, bot, document.file_id, document.file_size, document.file_name)


@router.message(F.document)
async def handle_document_auto(message: Message, bot: Bot):
    document = message.document
    
    if is_audio_file(document.file_name, document.mime_type):
        await process_audio_to_voice(message, bot, document.file_id, document.file_size, document.file_name)
        return
    
    if is_video_file(document.file_name, document.mime_type):
        from bot.handlers.video import process_video_to_circle
        await process_video_to_circle(message, bot, document.file_id, document.file_size, document.file_name)
        return
