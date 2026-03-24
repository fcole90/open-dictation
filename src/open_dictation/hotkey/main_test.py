from unittest.mock import MagicMock, patch

from open_dictation.hotkey.main import HotkeyListener


class TestHotkeyListenerParsing:
    """Test hotkey parsing functionality."""

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_parse_valid_hotkey(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test parsing a valid hotkey like 'f4'."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        listener = HotkeyListener(
            on_press_callback=lambda: None,
            on_release_callback=lambda: None,
        )

        assert listener.hotkey == mock_key

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_parse_invalid_hotkey(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test parsing an invalid hotkey returns None."""
        mock_settings.HOTKEY = "invalid_key"
        # Configure keyboard.Key to not have the invalid_key attribute
        mock_keyboard.Key = MagicMock(spec=[])  # Empty spec means no attributes

        with patch("open_dictation.hotkey.main.logger"):
            listener = HotkeyListener(
                on_press_callback=lambda: None,
                on_release_callback=lambda: None,
            )

        assert listener.hotkey is None

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_parse_hotkey_with_error_logging(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that invalid hotkey logs an error."""
        mock_settings.HOTKEY = "bad_hotkey"
        # Configure keyboard.Key to not have the bad_hotkey attribute
        mock_keyboard.Key = MagicMock(spec=[])  # Empty spec means no attributes

        with patch("open_dictation.hotkey.main.logger") as mock_logger:
            listener = HotkeyListener(  # type: ignore[reportUnusedVariable]
                on_press_callback=lambda: None,
                on_release_callback=lambda: None,
            )
            mock_logger.error.assert_called_once()


class TestHotkeyListenerCallbacks:
    """Test hotkey press/release callbacks."""

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_on_press_invokes_callback(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that pressing the hotkey invokes the press callback."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]

        press_callback.assert_called_once()
        release_callback.assert_not_called()

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_on_release_invokes_callback(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that releasing the hotkey invokes the release callback."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        # First press
        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]
        # Then release
        listener._on_release(mock_key)  # type: ignore[reportPrivateUsage]

        press_callback.assert_called_once()
        release_callback.assert_called_once()

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_release_without_prior_press(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that release without prior press doesn't invoke callback."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        # Release without pressing
        listener._on_release(mock_key)  # type: ignore[reportPrivateUsage]

        press_callback.assert_not_called()
        release_callback.assert_not_called()


class TestHotkeyListenerDebouncing:
    """Test hotkey debouncing functionality."""

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_multiple_presses_debounced(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that multiple presses without release are debounced."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        # First press
        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]
        # Second press (should be ignored due to debouncing)
        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]

        # Only called once
        assert press_callback.call_count == 1
        release_callback.assert_not_called()

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_press_release_press_sequence(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test press-release-press sequence triggers callbacks twice."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_keyboard.Key.f4 = mock_key

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        # First press
        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]
        # Release
        listener._on_release(mock_key)  # type: ignore[reportPrivateUsage]
        # Second press
        listener._on_press(mock_key)  # type: ignore[reportPrivateUsage]

        assert press_callback.call_count == 2
        assert release_callback.call_count == 1


class TestHotkeyListenerWrongKey:
    """Test behavior when non-hotkey is pressed."""

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_wrong_key_press_ignored(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that pressing wrong key doesn't invoke callbacks."""
        mock_settings.HOTKEY = "f4"
        mock_key_f4 = MagicMock()
        mock_key_f5 = MagicMock()
        mock_keyboard.Key.f4 = mock_key_f4

        press_callback = MagicMock()
        release_callback = MagicMock()

        listener = HotkeyListener(
            on_press_callback=press_callback,
            on_release_callback=release_callback,
        )

        # Press wrong key
        listener._on_press(mock_key_f5)  # type: ignore[reportPrivateUsage]

        press_callback.assert_not_called()
        release_callback.assert_not_called()


class TestHotkeyListenerLifecycle:
    """Test hotkey listener start/stop lifecycle."""

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_start_listener(self, mock_keyboard: MagicMock, mock_settings: MagicMock):
        """Test starting the listener."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_listener = MagicMock()
        mock_keyboard.Key.f4 = mock_key
        mock_keyboard.Listener = MagicMock(return_value=mock_listener)

        listener = HotkeyListener(
            on_press_callback=lambda: None,
            on_release_callback=lambda: None,
        )

        listener.start()

        mock_listener.start.assert_called_once()

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_stop_listener(self, mock_keyboard: MagicMock, mock_settings: MagicMock):
        """Test stopping the listener."""
        mock_settings.HOTKEY = "f4"
        mock_key = MagicMock()
        mock_listener = MagicMock()
        mock_keyboard.Key.f4 = mock_key
        mock_keyboard.Listener = MagicMock(return_value=mock_listener)

        listener = HotkeyListener(
            on_press_callback=lambda: None,
            on_release_callback=lambda: None,
        )

        listener.stop()

        mock_listener.stop.assert_called_once()

    @patch("open_dictation.hotkey.main.settings")
    @patch("open_dictation.hotkey.main.keyboard")
    def test_start_stop_without_valid_hotkey(
        self, mock_keyboard: MagicMock, mock_settings: MagicMock
    ):
        """Test that start/stop work gracefully without valid hotkey."""
        mock_settings.HOTKEY = "invalid"
        mock_keyboard.Key = MagicMock(spec=[])  # Empty spec means no attributes

        with patch("open_dictation.hotkey.main.logger"):
            listener = HotkeyListener(
                on_press_callback=lambda: None,
                on_release_callback=lambda: None,
            )

        # Should not raise
        listener.start()
        listener.stop()
