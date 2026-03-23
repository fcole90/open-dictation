from faster_whisper import WhisperModel  # type: ignore
import numpy as np
from numpy.typing import NDArray

from open_dictation.config import settings


class SpeechToText:
    def __init__(self, device: str = "cpu"):
        self.model = WhisperModel(
            settings.MODEL_SIZE, device=device, compute_type="int8"
        )

    def transcribe(self, audio: NDArray[np.float32]) -> str:
        """
        Transcribes an audio waveform and returns the full text.
        """
        segments, _ = self.model.transcribe(audio, beam_size=5)
        return " ".join([segment.text for segment in segments])
