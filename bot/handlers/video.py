import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.config import config
from bot.services.converter import ConversionService
from bot.utils.temp_file import TempFileManager
from bot.utils.media_detect import is_video_file, get_extension
from bot.states import UserState

router = Router()
semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
converter = ConversionService()


async def process_video_to_circle(message: Message, bot: Bot, file_id: str, file_size: int, filename: str | None):
    if file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю видео...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = get_extension(filename, ".mp4")
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".mp4")
            
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, input_path)
            
            await status_message.edit_text("Конвертирую в кружок...")
            
            result = await converter.convert_to_video_note(
                input_path,
                output_path,
                config.video_note_size,
                config.max_video_duration
            )
            
            if not result.success:
                await status_message.edit_text(f"Ошибка конвертации: {result.error}")
                return
            
            warning_text = ""
            if result.was_trimmed:
                warning_text = f"\n\nВидео было обрезано до {config.max_video_duration} секунд."
            
            await status_message.edit_text(f"Отправляю кружок...{warning_text}")
            
            video_note_file = FSInputFile(output_path)
            await message.reply_video_note(
                video_note=video_note_file,
                duration=min(result.duration, config.max_video_duration),
                length=config.video_note_size
            )
            
            final_text = "Готово!"
            if result.was_trimmed:
                final_text += f"\n\nВидео было обрезано с {result.original_duration} до {config.max_video_duration} секунд."
            
            await status_message.edit_text(final_text)
            
        except Exception as e:
            await status_message.edit_text(f"Произошла ошибка: {str(e)}")
        
        finally:
            temp_manager.cleanup(input_path)
            temp_manager.cleanup(output_path)


async def process_video_to_audio(message: Message, bot: Bot, file_id: str, file_size: int, filename: str | None):
    if file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю видео...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = get_extension(filename, ".mp4")
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".ogg")
            
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, input_path)
            
            await status_message.edit_text("Извлекаю аудио...")
            
            result = await converter.extract_audio_from_video(input_path, output_path)
            
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


@router.message(F.video, UserState.video_to_circle)
async def handle_video_circle_mode(message: Message, bot: Bot):
    video = message.video
    await process_video_to_circle(message, bot, video.file_id, video.file_size, video.file_name)


@router.message(F.video, UserState.video_to_audio)
async def handle_video_audio_mode(message: Message, bot: Bot):
    video = message.video
    await process_video_to_audio(message, bot, video.file_id, video.file_size, video.file_name)


@router.message(F.video)
async def handle_video_auto(message: Message, bot: Bot):
    video = message.video
    await process_video_to_circle(message, bot, video.file_id, video.file_size, video.file_name)


@router.message(F.document, UserState.video_to_circle)
async def handle_document_circle_mode(message: Message, bot: Bot):
    document = message.document
    if not is_video_file(document.file_name, document.mime_type):
        await message.reply(
            "Это не видеофайл.\n"
            "Поддерживаемые форматы: mp4, mov, avi, mkv, webm"
        )
        return
    await process_video_to_circle(message, bot, document.file_id, document.file_size, document.file_name)


@router.message(F.document, UserState.video_to_audio)
async def handle_document_audio_mode(message: Message, bot: Bot):
    document = message.document
    if not is_video_file(document.file_name, document.mime_type):
        await message.reply(
            "Это не видеофайл.\n"
            "Поддерживаемые форматы: mp4, mov, avi, mkv, webm"
        )
        return
    await process_video_to_audio(message, bot, document.file_id, document.file_size, document.file_name)
