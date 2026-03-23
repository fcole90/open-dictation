import threading
from faster_whisper import WhisperModel  # type: ignore
import numpy as np
from numpy.typing import NDArray

from open_dictation.config import settings
from open_dictation.logger import logger


class SpeechToText:
    def __init__(self):
        self.model: WhisperModel | None = None
        self.model_loaded = threading.Event()
        self._load_model_thread = threading.Thread(target=self._load_model)
        self._load_model_thread.daemon = True
        self._load_model_thread.start()

    def _load_model(self):
        logger.info(f"Loading Whisper model '{settings.MODEL_SIZE}'...")
        try:
            self.model = WhisperModel(
                settings.MODEL_SIZE,
                device=settings.COMPUTE_DEVICE,
                compute_type="int8",
            )
            self.model_loaded.set()
            logger.info("Whisper model loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            self.model = None

    def transcribe(self, audio: NDArray[np.float32]) -> str:
        """
        Transcribes an audio waveform and returns the full text.
        """
        if not self.model_loaded.is_set() or not self.model:
            logger.warning("Transcription called before model is loaded.")
            return ""
        try:
            segments, _ = self.model.transcribe(audio, beam_size=5)
            return " ".join([segment.text for segment in segments])
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return ""
