import pyperclip
from pynput.keyboard import Controller, Key


class TextInjector:
    def __init__(self):
        self._keyboard = Controller()

    def inject(self, text: str):
        """
        Injects the given text by copying it to the clipboard and simulating a paste command.
        """
        pyperclip.copy(text)
        with self._keyboard.pressed(Key.ctrl):
            self._keyboard.press("v")
            self._keyboard.release("v")
