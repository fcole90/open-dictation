from faster_whisper import WhisperModel  # type: ignore
import numpy as np
from numpy.typing import NDArray

from open_dictation.config import settings
from open_dictation.logger import logger


class SpeechToText:
    def __init__(self):
        try:
            self.model = WhisperModel(
                settings.MODEL_SIZE,
                device=settings.COMPUTE_DEVICE,
                compute_type="int8",
            )
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            self.model = None

    def transcribe(self, audio: NDArray[np.float32]) -> str:
        """
        Transcribes an audio waveform and returns the full text.
        """
        if not self.model:
            return ""
        try:
            segments, _ = self.model.transcribe(audio, beam_size=5)
            return " ".join([segment.text for segment in segments])
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return ""
