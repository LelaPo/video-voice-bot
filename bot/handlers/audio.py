import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from bot.config import config
from bot.services.converter import ConversionService
from bot.utils.temp_file import TempFileManager

router = Router()
semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
converter = ConversionService()

SUPPORTED_AUDIO = ["audio/mpeg", "audio/wav", "audio/x-wav", "audio/mp4", "audio/m4a", "audio/ogg", "audio/flac"]


@router.message(F.audio)
async def handle_audio(message: Message, bot: Bot):
    audio = message.audio
    
    if audio.file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {audio.file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю аудио...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = ".mp3"
            if audio.file_name:
                parts = audio.file_name.rsplit(".", 1)
                if len(parts) > 1:
                    ext = f".{parts[1]}"
            
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".ogg")
            
            file = await bot.get_file(audio.file_id)
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


@router.message(F.document)
async def handle_audio_document(message: Message, bot: Bot):
    document = message.document
    
    if not document.mime_type:
        return
    
    if not document.mime_type.startswith("audio/"):
        return
    
    if document.file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {document.file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю аудио...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = ".mp3"
            if document.file_name:
                parts = document.file_name.rsplit(".", 1)
                if len(parts) > 1:
                    ext = f".{parts[1]}"
            
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".ogg")
            
            file = await bot.get_file(document.file_id)
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
