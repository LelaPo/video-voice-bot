import asyncio
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConversionResult:
    success: bool
    duration: int = 0
    original_duration: int = 0
    was_trimmed: bool = False
    error: str = ""


class ConversionService:
    
    async def get_media_duration(self, input_path: str) -> int:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            input_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, _ = await process.communicate()
        
        if process.returncode != 0:
            return 0
        
        try:
            data = json.loads(stdout.decode())
            duration = float(data.get("format", {}).get("duration", 0))
            return int(duration)
        except (json.JSONDecodeError, ValueError, KeyError):
            return 0
    
    async def convert_to_video_note(
        self,
        input_path: str,
        output_path: str,
        size: int,
        max_duration: int
    ) -> ConversionResult:
        
        original_duration = await self.get_media_duration(input_path)
        was_trimmed = original_duration > max_duration
        
        duration_args = []
        if was_trimmed:
            duration_args = ["-t", str(max_duration)]
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            *duration_args,
            "-vf", f"crop=min(iw\\,ih):min(iw\\,ih),scale={size}:{size}",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            "-pix_fmt", "yuv420p",
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        _, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_text = stderr.decode() if stderr else "Unknown error"
            return ConversionResult(
                success=False,
                error=error_text[:500]
            )
        
        if not Path(output_path).exists():
            return ConversionResult(
                success=False,
                error="Output file was not created"
            )
        
        final_duration = await self.get_media_duration(output_path)
        
        return ConversionResult(
            success=True,
            duration=final_duration,
            original_duration=original_duration,
            was_trimmed=was_trimmed
        )
    
    async def convert_to_voice(
        self,
        input_path: str,
        output_path: str
    ) -> ConversionResult:
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-c:a", "libopus",
            "-b:a", "64k",
            "-vbr", "on",
            "-compression_level", "10",
            "-application", "voip",
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        _, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_text = stderr.decode() if stderr else "Unknown error"
            return ConversionResult(
                success=False,
                error=error_text[:500]
            )
        
        if not Path(output_path).exists():
            return ConversionResult(
                success=False,
                error="Output file was not created"
            )
        
        duration = await self.get_media_duration(output_path)
        
        return ConversionResult(
            success=True,
            duration=duration
        )
    
    async def extract_audio_from_video(
        self,
        input_path: str,
        output_path: str
    ) -> ConversionResult:
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-vn",
            "-c:a", "libopus",
            "-b:a", "64k",
            "-vbr", "on",
            "-compression_level", "10",
            "-application", "voip",
            output_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        _, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_text = stderr.decode() if stderr else "Unknown error"
            if "does not contain any stream" in error_text or "Output file is empty" in error_text:
                return ConversionResult(
                    success=False,
                    error="Видео не содержит аудиодорожки"
                )
            return ConversionResult(
                success=False,
                error=error_text[:500]
            )
        
        if not Path(output_path).exists():
            return ConversionResult(
                success=False,
                error="Output file was not created"
            )
        
        duration = await self.get_media_duration(output_path)
        
        return ConversionResult(
            success=True,
            duration=duration
        )
