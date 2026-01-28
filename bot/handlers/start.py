from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main import get_main_keyboard, get_mode_keyboard
from bot.states import UserState

router = Router()

WELCOME_TEXT = """
<b>Конвертер видео и аудио</b>

Этот бот умеет:
• Превращать видео в кружки (video note)
• Превращать аудио в голосовые сообщения
• Извлекать аудио из видео

<b>Автоматический режим:</b>
Просто отправьте файл — видео станет кружком, аудио станет голосовым.

<b>Ограничения:</b>
• Максимальный размер файла: 20 МБ
• Максимальная длительность видео: 60 секунд
• Видео длиннее 60 секунд будет обрезано

Или выберите специальный режим:
"""

CIRCLE_MODE_TEXT = """
<b>Режим: Видео в кружок</b>

Отправьте видеофайл (mp4, mov, avi, mkv, webm).

Видео будет конвертировано в квадратный формат и отправлено как кружок.

Для возврата в автоматический режим нажмите "Сбросить режим".
"""

VOICE_MODE_TEXT = """
<b>Режим: Аудио в голосовое</b>

Отправьте аудиофайл (mp3, wav, m4a, ogg, flac).

Аудио будет конвертировано и отправлено как голосовое сообщение.

Для возврата в автоматический режим нажмите "Сбросить режим".
"""

VIDEO_TO_AUDIO_MODE_TEXT = """
<b>Режим: Видео в аудио</b>

Отправьте видеофайл (mp4, mov, avi, mkv, webm).

Звуковая дорожка будет извлечена и отправлена как голосовое сообщение.

Для возврата в автоматический режим нажмите "Сбросить режим".
"""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=get_main_keyboard())


@router.message(Command("circle"))
async def cmd_circle(message: Message, state: FSMContext):
    await state.set_state(UserState.video_to_circle)
    await message.answer(CIRCLE_MODE_TEXT, reply_markup=get_mode_keyboard())


@router.message(Command("voice"))
async def cmd_voice(message: Message, state: FSMContext):
    await state.set_state(UserState.audio_to_voice)
    await message.answer(VOICE_MODE_TEXT, reply_markup=get_mode_keyboard())


@router.message(Command("extract"))
async def cmd_extract(message: Message, state: FSMContext):
    await state.set_state(UserState.video_to_audio)
    await message.answer(VIDEO_TO_AUDIO_MODE_TEXT, reply_markup=get_mode_keyboard())
