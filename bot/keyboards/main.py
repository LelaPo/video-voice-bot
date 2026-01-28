from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Видео → Кружок",
                callback_data="mode_circle"
            )
        ],
        [
            InlineKeyboardButton(
                text="Аудио → Голосовое",
                callback_data="mode_voice"
            )
        ],
        [
            InlineKeyboardButton(
                text="Видео → Аудио",
                callback_data="mode_video_to_audio"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_mode_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text="Сбросить режим",
                callback_data="reset_mode"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
