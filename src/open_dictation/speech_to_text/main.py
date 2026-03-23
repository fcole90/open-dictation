from faster_whisper import WhisperModel
import numpy as np


class SpeechToText:
    def __init__(self, model_name: str = "base.en", device: str = "cpu"):
        self.model = WhisperModel(model_name, device=device, compute_type="int8")

    def transcribe(
        self, audio: np.ndarray[np.float32, np.dtype[np.float32]]
    ) -> str:
        """
        Transcribes an audio waveform and returns the full text.
        """
        segments, _ = self.model.transcribe(audio, beam_size=5)
        return " ".join([segment.text for segment in segments])
