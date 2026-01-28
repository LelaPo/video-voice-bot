from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.main import get_main_keyboard, get_mode_keyboard
from bot.handlers.start import (
    WELCOME_TEXT,
    CIRCLE_MODE_TEXT,
    VOICE_MODE_TEXT,
    VIDEO_TO_AUDIO_MODE_TEXT,
)
from bot.states import UserState

router = Router()


@router.callback_query(F.data == "mode_circle")
async def callback_mode_circle(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.video_to_circle)
    await callback.message.edit_text(CIRCLE_MODE_TEXT, reply_markup=get_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "mode_voice")
async def callback_mode_voice(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.audio_to_voice)
    await callback.message.edit_text(VOICE_MODE_TEXT, reply_markup=get_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "mode_video_to_audio")
async def callback_mode_video_to_audio(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.video_to_audio)
    await callback.message.edit_text(VIDEO_TO_AUDIO_MODE_TEXT, reply_markup=get_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "reset_mode")
async def callback_reset_mode(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=get_main_keyboard())
    await callback.answer("Автоматический режим включен")
