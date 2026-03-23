from pynput import keyboard
from typing import Callable, Optional

from open_dictation.config import settings
from open_dictation.logger import logger


class HotkeyListener:
    def __init__(
        self,
        on_press_callback: Callable[[], None],
        on_release_callback: Callable[[], None],
    ):
        self._on_press_callback = on_press_callback
        self._on_release_callback = on_release_callback
        self.hotkey = self._parse_hotkey(settings.HOTKEY)
        if self.hotkey:
            self._listener = keyboard.Listener(
                on_press=self._on_press, on_release=self._on_release
            )
        self._hotkey_pressed = False

    def _parse_hotkey(self, hotkey_str: str) -> Optional[keyboard.Key]:
        try:
            key = getattr(keyboard.Key, hotkey_str, None)
            if key is None:
                raise ValueError(f"Unsupported hotkey: {hotkey_str}")
            return key
        except (ValueError, AttributeError) as e:
            logger.error(f"Invalid hotkey '{hotkey_str}': {e}")
            return None

    def _on_press(self, key: Optional[keyboard.Key | keyboard.KeyCode]):
        if key == self.hotkey and not self._hotkey_pressed:
            self._hotkey_pressed = True
            self._on_press_callback()

    def _on_release(self, key: Optional[keyboard.Key | keyboard.KeyCode]):
        if key == self.hotkey:
            if self._hotkey_pressed:
                self._hotkey_pressed = False
                self._on_release_callback()

    def start(self):
        """Starts the hotkey listener in a non-blocking way."""
        if hasattr(self, "_listener"):
            self._listener.start()

    def stop(self):
        """Stops the hotkey listener."""
        if hasattr(self, "_listener"):
            self._listener.stop()
