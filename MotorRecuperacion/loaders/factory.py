import os
from typing import Optional
from .base import BaseFileLoader
from .text_loader import TextHandler
from .pdf_loader import PdfHandler
from .docx_loader import DocxHandler
from .image_loader import ImageHandler
from .video_loader import VideoHandler

class FileLoaderFactory:
    """Factory to get the appropriate loader for a file extension."""
    
    _LOADERS = {
        ".txt": TextHandler(),
        ".md": TextHandler(),
        ".py": TextHandler(),
        ".json": TextHandler(),
        ".pdf": PdfHandler(),
        ".docx": DocxHandler(),
        ".jpg": ImageHandler(),
        ".jpeg": ImageHandler(),
        ".png": ImageHandler(),
        ".bmp": ImageHandler(),
        ".mp4": VideoHandler(),
        ".avi": VideoHandler(),
        ".mov": VideoHandler(),
        ".mkv": VideoHandler(),
    }

    @staticmethod
    def get_loader(path: str) -> Optional[BaseFileLoader]:
        ext = os.path.splitext(path)[1].lower()
        return FileLoaderFactory._LOADERS.get(ext)
