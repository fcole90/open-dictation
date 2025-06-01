from os import path
from pathlib import Path
from pywhispercpp.model import Model  # type: ignore

__CURRENT_DIR__ = Path(__file__).parent.resolve()
__PKG_ROOT_DIR__ = __CURRENT_DIR__.resolve()


def get_transcription(model_name: str, audio_path: str):
    model = Model(model_name)
    return model.transcribe(audio_path)


def main():
    segments = get_transcription(
        "base.en",
        path.join(__PKG_ROOT_DIR__, "test_data", "Armstrong_Small_Step_16K.wav"),
    )
    for segment in segments:
        print(segment.text)

    segments = get_transcription(
        "base.en",
        path.join(
            __PKG_ROOT_DIR__, "..", "recording", "test_data", "voice_recording.wav"
        ),
    )
    for segment in segments:
        print(segment.text)


if __name__ == "__main__":
    main()
