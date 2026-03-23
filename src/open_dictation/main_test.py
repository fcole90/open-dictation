from unittest.mock import MagicMock, patch
import numpy as np
from open_dictation.main import OpenDictationApp


@patch("open_dictation.main.AudioRecorder")
@patch("open_dictation.main.SpeechToText")
@patch("open_dictation.main.TextInjector")
@patch("open_dictation.main.HotkeyListener")
@patch("open_dictation.main.TrayIcon")
def test_open_dictation_app_workflow(
    TrayIconMock: MagicMock,
    HotkeyListenerMock: MagicMock,
    TextInjectorMock: MagicMock,
    SpeechToTextMock: MagicMock,
    AudioRecorderMock: MagicMock,
):
    # Arrange
    app = OpenDictationApp()
    audio_recorder_mock = AudioRecorderMock.return_value
    stt_mock = SpeechToTextMock.return_value
    text_injector_mock = TextInjectorMock.return_value

    # Mock the return value of the audio recorder
    audio_data = np.random.rand(16000).astype(np.float32)
    audio_recorder_mock.stop.return_value = audio_data

    # Mock the return value of the speech-to-text
    stt_mock.transcribe.return_value = "Hello, world!"

    # Act
    app._on_hotkey_press()  # type: ignore[reportPrivateUsage]
    app._on_hotkey_release()  # type: ignore[reportPrivateUsage]

    # Assert
    audio_recorder_mock.start.assert_called_once()
    audio_recorder_mock.stop.assert_called_once()
    stt_mock.transcribe.assert_called_once()
    np.testing.assert_array_equal(
        stt_mock.transcribe.call_args[0][0], audio_data.flatten()
    )
    text_injector_mock.inject.assert_called_once_with("Hello, world!")
