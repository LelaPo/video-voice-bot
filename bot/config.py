from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str
    max_concurrent_tasks: int
    video_note_size: int
    max_video_duration: int
    max_file_size: int = 20 * 1024 * 1024
    temp_dir: str = "/tmp/bot_files"

    @classmethod
    def from_env(cls) -> "Config":
        token = getenv("BOT_TOKEN")
        if not token:
            raise ValueError("BOT_TOKEN is required")
        
        return cls(
            bot_token=token,
            max_concurrent_tasks=int(getenv("MAX_CONCURRENT_TASKS", "4")),
            video_note_size=int(getenv("VIDEO_NOTE_SIZE", "480")),
            max_video_duration=int(getenv("MAX_VIDEO_DURATION", "60")),
        )


config = Config.from_env()
