from pynput import keyboard
from typing import Callable, Optional


class HotkeyListener:
    def __init__(
        self,
        on_press_callback: Callable[[], None],
        on_release_callback: Callable[[], None],
        hotkey_str: str = "f4",
    ):
        self._on_press_callback = on_press_callback
        self._on_release_callback = on_release_callback
        self.hotkey = self._parse_hotkey(hotkey_str)
        self._listener = keyboard.Listener(
            on_press=self._on_press, on_release=self._on_release
        )
        self._hotkey_pressed = False

    def _parse_hotkey(self, hotkey_str: str) -> keyboard.Key:
        key = getattr(keyboard.Key, hotkey_str, None)
        if key is None:
            raise ValueError(f"Unsupported hotkey: {hotkey_str}")
        return key

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
        self._listener.start()

    def stop(self):
        """Stops the hotkey listener."""
        self._listener.stop()
