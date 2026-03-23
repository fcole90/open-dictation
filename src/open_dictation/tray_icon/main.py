from pystray.icon import Icon  # type: ignore
from pystray import Menu, MenuItem  # type: ignore
from PIL import Image
from typing import Callable


class TrayIcon:
    def __init__(self, name: str, on_quit: Callable[[], None]):
        self._on_quit = on_quit
        self._icon: Icon = self._create_icon(name)

    def _create_icon(self, name: str) -> Icon:
        image = Image.new("RGB", (64, 64), "black")
        menu = Menu(MenuItem("Quit", self._on_quit_clicked))
        return Icon(name, image, name, menu)

    def _on_quit_clicked(self) -> None:
        self.stop()
        self._on_quit()

    def start(self) -> None:
        """Starts the tray icon in a non-blocking way."""
        self._icon.run_detached()

    def stop(self) -> None:
        """Stops the tray icon."""
        self._icon.stop()
