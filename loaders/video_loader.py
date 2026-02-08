import os
import tempfile
from typing import List
from langchain_core.documents import Document
from .base import BaseFileLoader

try:
    import whisper
    from moviepy import VideoFileClip
    VIDEO_SUPPORT = True
except ImportError:
    VIDEO_SUPPORT = False

class VideoHandler(BaseFileLoader):
    def __init__(self):
        self.whisper_model = None

    def _get_model(self):
        if self.whisper_model is None:
            print("Cargando modelo Whisper...")
            self.whisper_model = whisper.load_model("base")
        return self.whisper_model

    def load(self, path: str) -> List[Document]:
        if not VIDEO_SUPPORT:
            print("Video support not available. Install 'openai-whisper' and 'moviepy'.")
            return [Document(page_content="[Video support disabled]", metadata={"source": path})]

        try:
            model = self._get_model()
            
            # Extraer audio temporalmente
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio:
                tmp_audio_path = tmp_audio.name
            
            video = VideoFileClip(path)
            # Suppress moviepy output
            video.audio.write_audiofile(tmp_audio_path, verbose=False, logger=None)
            video.close()

            # Transcribir
            print(f"Transcribiendo video: {path} ...")
            result = model.transcribe(tmp_audio_path)
            text = result["text"]

            # Limpiar
            os.remove(tmp_audio_path)
            return [Document(page_content=text, metadata={"source": path})]

        except Exception as e:
            print(f"Error procesando video {path}: {e}")
            return []
