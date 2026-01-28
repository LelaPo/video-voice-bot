from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    video_to_circle = State()
    audio_to_voice = State()
    video_to_audio = State()
