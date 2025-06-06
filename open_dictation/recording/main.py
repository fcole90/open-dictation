import os
from pathlib import Path
from typing import cast
import numpy
import sounddevice  # type: ignore
import wavio as wavio  # type: ignore

__CURRENT_DIR__ = Path(__file__).parent.resolve()
__PKG_ROOT_DIR__ = __CURRENT_DIR__.resolve()


def __change_dir_to_pkg_root() -> None:
    """
    Change the current working directory to the package root directory.
    This is useful for ensuring relative paths work correctly.
    """
    os.chdir(__PKG_ROOT_DIR__)
    print(f"Changed working directory to: {__PKG_ROOT_DIR__}")


def record(duration: int, frequency: int = 16000, channels: int = 2):
    recording = cast(
        numpy.typing.NDArray[numpy.float32],
        sounddevice.rec(
            int(duration * frequency), samplerate=frequency, channels=channels
        ),
    )
    sounddevice.wait()
    return recording


def main():
    frequency = 16000
    duration = 5
    channels = 2

    TEST_DATA_DIR = __PKG_ROOT_DIR__.joinpath("test_data")

    __change_dir_to_pkg_root()

    input(f"Press enter when ready to record for {duration} seconds.")
    print("Recording started...")
    recording = record(duration=duration, frequency=frequency)
    print("Recording finished...")

    print("Saving...")
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    wavio.write(
        str(TEST_DATA_DIR.joinpath("voice_recording.wav")),
        recording,
        frequency,
        sampwidth=channels,
    )
    print("Done")


if __name__ == "__main__":
    main()
