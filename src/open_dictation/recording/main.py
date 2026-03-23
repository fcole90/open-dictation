import numpy as np
import sounddevice as sd  # type: ignore
from typing import Any, List
from numpy.typing import NDArray


class AudioRecorder:
    def __init__(self, frequency: int = 16000, channels: int = 1):
        self.frequency = frequency
        self.channels = channels
        self._frames: List[NDArray[np.float32]] = []
        self._stream: sd.InputStream | None = None

    def _callback(
        self, indata: NDArray[np.float32], frames: int, time: Any, status: Any
    ) -> None:
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

    def stop(self) -> NDArray[np.float32]:
        """Stops the recording stream and returns the audio data."""
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            if self._frames:
                return np.concatenate(self._frames)
        return np.array([], dtype=np.float32)
