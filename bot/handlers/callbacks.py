from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.main import get_main_keyboard, get_mode_keyboard
from bot.handlers.start import WELCOME_TEXT, CIRCLE_MODE_TEXT, VOICE_MODE_TEXT

router = Router()


@router.callback_query(F.data == "mode_circle")
async def callback_mode_circle(callback: CallbackQuery):
    await callback.message.edit_text(CIRCLE_MODE_TEXT, reply_markup=get_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "mode_voice")
async def callback_mode_voice(callback: CallbackQuery):
    await callback.message.edit_text(VOICE_MODE_TEXT, reply_markup=get_mode_keyboard())
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def callback_back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=get_main_keyboard())
    await callback.answer()
