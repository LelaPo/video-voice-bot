from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v", ".3gp", ".flv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma", ".opus"}

VIDEO_MIME_PREFIXES = ("video/",)
AUDIO_MIME_PREFIXES = ("audio/",)


def is_video_file(filename: str | None, mime_type: str | None) -> bool:
    if filename:
        ext = Path(filename).suffix.lower()
        if ext in VIDEO_EXTENSIONS:
            return True
    
    if mime_type:
        if mime_type.startswith(VIDEO_MIME_PREFIXES):
            return True
    
    return False


def is_audio_file(filename: str | None, mime_type: str | None) -> bool:
    if filename:
        ext = Path(filename).suffix.lower()
        if ext in AUDIO_EXTENSIONS:
            return True
    
    if mime_type:
        if mime_type.startswith(AUDIO_MIME_PREFIXES):
            return True
    
    return False


def get_extension(filename: str | None, default: str) -> str:
    if filename:
        ext = Path(filename).suffix.lower()
        if ext:
            return ext
    return default
