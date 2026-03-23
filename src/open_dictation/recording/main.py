import numpy as np
import sounddevice as sd
from typing import List


class AudioRecorder:
    def __init__(self, frequency: int = 16000, channels: int = 1):
        self.frequency = frequency
        self.channels = channels
        self._frames: List[np.ndarray] = []
        self._stream: sd.InputStream | None = None

    def _callback(self, indata: np.ndarray, frames: int, time, status):
        """This is called (from a separate thread) for each audio block."""
        self._frames.append(indata.copy())

    def start(self) -> None:
        """Starts a non-blocking recording stream."""
        self._frames = []
        self._stream = sd.InputStream(
            samplerate=self.frequency,
            channels=self.channels,
            callback=self._callback,
            dtype="float32",
        )
        self._stream.start()

    def stop(self) -> np.ndarray:
        """Stops the recording stream and returns the audio data."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            return np.concatenate(self._frames)
        return np.array([], dtype=np.float32)
