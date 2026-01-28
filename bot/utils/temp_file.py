import uuid
from pathlib import Path

from bot.config import config


class TempFileManager:
    
    def __init__(self):
        self.temp_dir = Path(config.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def create_temp_path(self, prefix: str, extension: str) -> str:
        filename = f"{prefix}_{uuid.uuid4().hex}{extension}"
        return str(self.temp_dir / filename)
    
    def cleanup(self, file_path: str | None):
        if file_path is None:
            return
        
        path = Path(file_path)
        if path.exists():
            try:
                path.unlink()
            except OSError:
                pass
