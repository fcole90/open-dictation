import threading
import time
from unittest.mock import MagicMock, patch

from open_dictation.main import OpenDictationApp


class TestOpenDictationAppIntegration:
    """Integration tests for the complete OpenDictationApp workflow."""

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_initialization(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that app initializes all components correctly."""
        app: OpenDictationApp = OpenDictationApp()

        assert app.recorder is not None
        assert app.stt is not None
        assert app.injector is not None
        assert app.hotkey_listener is not None
        assert app.tray_icon is not None
        assert app._running is False  # type: ignore[reportPrivateUsage]

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_startup_and_shutdown(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that app starts and stops gracefully without errors."""
        app = OpenDictationApp()

        # Start app in a separate thread
        app_thread = threading.Thread(target=self._run_app_briefly, args=(app,))
        app_thread.start()

        # Wait for app to start
        time.sleep(0.5)

        # Verify app is running
        assert app._running is True  # type: ignore[reportPrivateUsage]

        # Stop the app
        app.stop()
        app_thread.join(timeout=5)

        # Verify app stopped
        assert app._running is False  # type: ignore[reportPrivateUsage]

        # Verify all components' stop methods were called
        mock_hotkey_listener.return_value.stop.assert_called()
        mock_tray_icon.return_value.stop.assert_called()

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_hotkey_triggers_recording(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that hotkey press/release triggers recording workflow."""
        import numpy as np

        # Setup mocks
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_audio_recorder.return_value.stop.return_value = audio_data
        mock_stt.return_value.transcribe.return_value = "Test transcription"

        app: OpenDictationApp = OpenDictationApp()
        assert app.stt is not None  # Verify app initialized

        # Get the hotkey callbacks
        hotkey_listener_init = mock_hotkey_listener.call_args
        on_press_callback = hotkey_listener_init[1]["on_press_callback"]
        on_release_callback = hotkey_listener_init[1]["on_release_callback"]

        # Simulate hotkey press and release
        on_press_callback()
        on_release_callback()

        # Verify recording workflow was triggered
        mock_audio_recorder.return_value.start.assert_called()
        mock_audio_recorder.return_value.stop.assert_called()
        mock_stt.return_value.transcribe.assert_called()
        mock_text_injector.return_value.inject.assert_called_with("Test transcription")

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_handles_transcription_error(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that app handles transcription errors gracefully."""
        import numpy as np

        # Setup mocks
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_audio_recorder.return_value.stop.return_value = audio_data
        mock_stt.return_value.transcribe.return_value = ""  # Empty transcription

        app: OpenDictationApp = OpenDictationApp()
        assert app.injector is not None  # Verify app initialized

        # Get the hotkey callbacks
        hotkey_listener_init = mock_hotkey_listener.call_args
        on_release_callback = hotkey_listener_init[1]["on_release_callback"]

        # Mock the press to set up state
        on_press_callback = hotkey_listener_init[1]["on_press_callback"]
        on_press_callback()

        # Simulate release (should handle empty transcription)
        on_release_callback()

        # Verify no injection if transcription is empty
        mock_text_injector.return_value.inject.assert_not_called()

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_handles_empty_audio(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that app handles empty audio data gracefully."""
        import numpy as np

        # Setup mocks with empty audio
        empty_audio = np.array([], dtype=np.float32)
        mock_audio_recorder.return_value.stop.return_value = empty_audio

        app: OpenDictationApp = OpenDictationApp()
        assert app.recorder is not None  # Verify app initialized

        # Get the hotkey callbacks
        hotkey_listener_init = mock_hotkey_listener.call_args
        on_press_callback = hotkey_listener_init[1]["on_press_callback"]
        on_release_callback = hotkey_listener_init[1]["on_release_callback"]

        # Simulate press and release
        on_press_callback()
        on_release_callback()

        # Verify transcription wasn't called for empty audio
        mock_stt.return_value.transcribe.assert_not_called()

    @patch("open_dictation.main.AudioRecorder")
    @patch("open_dictation.main.SpeechToText")
    @patch("open_dictation.main.TextInjector")
    @patch("open_dictation.main.HotkeyListener")
    @patch("open_dictation.main.TrayIcon")
    def test_app_tray_icon_status_updates(
        self,
        mock_tray_icon: MagicMock,
        mock_hotkey_listener: MagicMock,
        mock_text_injector: MagicMock,
        mock_stt: MagicMock,
        mock_audio_recorder: MagicMock,
    ):
        """Test that tray icon status is updated during recording workflow."""
        import numpy as np

        # Setup mocks
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        mock_audio_recorder.return_value.stop.return_value = audio_data
        mock_stt.return_value.transcribe.return_value = "Test"

        app: OpenDictationApp = OpenDictationApp()
        assert app.tray_icon is not None  # Verify app initialized

        # Get the hotkey callbacks
        hotkey_listener_init = mock_hotkey_listener.call_args
        on_press_callback = hotkey_listener_init[1]["on_press_callback"]
        on_release_callback = hotkey_listener_init[1]["on_release_callback"]

        # Reset to track calls
        mock_tray_icon.return_value.set_status.reset_mock()

        # Simulate hotkey press
        on_press_callback()
        mock_tray_icon.return_value.set_status.assert_called_with("Recording")

        # Simulate hotkey release
        on_release_callback()

        # Verify status updates: Transcribing -> Idle
        calls = mock_tray_icon.return_value.set_status.call_args_list
        assert any(call[0][0] == "Transcribing" for call in calls)
        assert any(call[0][0] == "Idle" for call in calls)

    @staticmethod
    def _run_app_briefly(app: OpenDictationApp, duration: float = 0.5) -> None:
        """Helper to run app for a brief period."""
        app._running = True  # type: ignore[reportPrivateUsage]
        start = time.time()
        while app._running and (time.time() - start) < duration:  # type: ignore[reportPrivateUsage]
            time.sleep(0.1)
