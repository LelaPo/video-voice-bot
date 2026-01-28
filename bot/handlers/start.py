from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.keyboards.main import get_main_keyboard, get_mode_keyboard

router = Router()

WELCOME_TEXT = """
<b>Конвертер видео и аудио</b>

Этот бот умеет:
• Превращать видео в кружки (video note)
• Превращать аудио в голосовые сообщения

<b>Ограничения:</b>
• Максимальный размер файла: 20 МБ
• Максимальная длительность видео: 60 секунд
• Видео длиннее 60 секунд будет обрезано

Выберите режим работы:
"""

CIRCLE_MODE_TEXT = """
<b>Режим: Видео в кружок</b>

Отправьте видеофайл (mp4, mov, avi, mkv, webm).

Видео будет конвертировано в квадратный формат и отправлено как кружок.

Для смены режима нажмите "Назад".
"""

VOICE_MODE_TEXT = """
<b>Режим: Аудио в голосовое</b>

Отправьте аудиофайл (mp3, wav, m4a, ogg, flac).

Аудио будет конвертировано и отправлено как голосовое сообщение.

Для смены режима нажмите "Назад".
"""


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.message(Command("circle"))
async def cmd_circle(message: Message):
    await message.answer(CIRCLE_MODE_TEXT, reply_markup=get_mode_keyboard())


@router.message(Command("voice"))
async def cmd_voice(message: Message):
    await message.answer(VOICE_MODE_TEXT, reply_markup=get_mode_keyboard())
