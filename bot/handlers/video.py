import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile

from bot.config import config
from bot.services.converter import ConversionService
from bot.utils.temp_file import TempFileManager

router = Router()
semaphore = asyncio.Semaphore(config.max_concurrent_tasks)
converter = ConversionService()

SUPPORTED_VIDEO = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/x-matroska", "video/webm"]


@router.message(F.video)
async def handle_video(message: Message, bot: Bot):
    video = message.video
    
    if video.file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {video.file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю видео...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            input_path = temp_manager.create_temp_path("input", ".mp4")
            output_path = temp_manager.create_temp_path("output", ".mp4")
            
            file = await bot.get_file(video.file_id)
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


@router.message(F.document)
async def handle_video_document(message: Message, bot: Bot):
    document = message.document
    
    if not document.mime_type:
        return
    
    if document.mime_type not in SUPPORTED_VIDEO and not document.mime_type.startswith("video/"):
        if document.mime_type.startswith("audio/"):
            return
        await message.reply(
            "Неподдерживаемый формат файла.\n"
            "Поддерживаемые форматы видео: mp4, mov, avi, mkv, webm\n"
            "Поддерживаемые форматы аудио: mp3, wav, m4a, ogg, flac"
        )
        return
    
    if document.file_size > config.max_file_size:
        await message.reply(
            f"Файл слишком большой.\n"
            f"Максимальный размер: {config.max_file_size // (1024 * 1024)} МБ\n"
            f"Ваш файл: {document.file_size // (1024 * 1024)} МБ"
        )
        return
    
    status_message = await message.reply("Обрабатываю видео...")
    
    async with semaphore:
        temp_manager = TempFileManager()
        input_path = None
        output_path = None
        
        try:
            ext = ".mp4"
            if document.file_name:
                parts = document.file_name.rsplit(".", 1)
                if len(parts) > 1:
                    ext = f".{parts[1]}"
            
            input_path = temp_manager.create_temp_path("input", ext)
            output_path = temp_manager.create_temp_path("output", ".mp4")
            
            file = await bot.get_file(document.file_id)
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
