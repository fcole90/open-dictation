from pynput import keyboard
from typing import Any, Callable, Optional

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
        self.hotkey_spec = self._parse_hotkey(settings.HOTKEY)
        if self.hotkey_spec:
            self._listener = keyboard.Listener(
                on_press=self._on_press, on_release=self._on_release
            )
        self._hotkey_pressed = False
        self._modifiers_pressed: set[str] = set()

    def _parse_hotkey(self, hotkey_str: str) -> Optional[dict[str, Any]]:
        """Parse hotkey string like 'shift+f5' or 'f4' into modifiers and main key."""
        try:
            parts = hotkey_str.lower().split("+")
            main_key = parts[-1]
            modifiers: set[str] = set(parts[:-1]) if len(parts) > 1 else set()

            # Verify main key exists
            if not hasattr(keyboard.Key, main_key):
                raise ValueError(f"Unsupported hotkey: {hotkey_str}")

            # Verify modifiers are valid
            valid_modifiers: set[str] = {"shift", "ctrl", "alt"}
            for mod in modifiers:
                if mod not in valid_modifiers:
                    raise ValueError(f"Unsupported modifier: {mod}")

            return {
                "main_key": main_key,
                "modifiers": modifiers,
                "original": hotkey_str,
            }
        except (ValueError, AttributeError) as e:
            logger.error(f"Invalid hotkey '{hotkey_str}': {e}")
            return None

    def _identify_modifier(
        self, key: Optional[keyboard.Key | keyboard.KeyCode]
    ) -> Optional[str]:
        """Identify which modifier a key represents, or None if not a modifier."""
        if key is None:
            return None

        if (hasattr(keyboard.Key, "shift") and key == keyboard.Key.shift) or (
            hasattr(keyboard.Key, "shift_r") and key == keyboard.Key.shift_r
        ):
            return "shift"
        elif (hasattr(keyboard.Key, "ctrl") and key == keyboard.Key.ctrl) or (
            hasattr(keyboard.Key, "ctrl_r") and key == keyboard.Key.ctrl_r
        ):
            return "ctrl"
        elif (hasattr(keyboard.Key, "alt") and key == keyboard.Key.alt) or (
            hasattr(keyboard.Key, "alt_r") and key == keyboard.Key.alt_r
        ):
            return "alt"
        return None

    def _update_modifier_state(
        self, key: Optional[keyboard.Key | keyboard.KeyCode], add: bool = True
    ) -> None:
        """Track or untrack a modifier key press/release."""
        modifier = self._identify_modifier(key)
        if modifier:
            if add:
                self._modifiers_pressed.add(modifier)
            else:
                self._modifiers_pressed.discard(modifier)

    def _on_press(self, key: Optional[keyboard.Key | keyboard.KeyCode]):
        if key is None or self.hotkey_spec is None:
            return

        # Track modifier keys
        self._update_modifier_state(key, add=True)

        # Check if main key matches
        main_key_attr = getattr(keyboard.Key, self.hotkey_spec["main_key"], None)
        if (
            key == main_key_attr
            and self._modifiers_pressed == self.hotkey_spec["modifiers"]
            and not self._hotkey_pressed
        ):
            self._hotkey_pressed = True
            self._on_press_callback()

    def _on_release(self, key: Optional[keyboard.Key | keyboard.KeyCode]):
        if key is None or self.hotkey_spec is None:
            return

        # Track modifier key releases
        self._update_modifier_state(key, add=False)

        # Check if main key was released
        main_key_attr = getattr(keyboard.Key, self.hotkey_spec["main_key"], None)
        if key == main_key_attr:
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
