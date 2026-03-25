from pystray import Icon, Menu, MenuItem  # type: ignore
from PIL import Image
from typing import Callable

from open_dictation.config import settings


class TrayIcon:
    def __init__(self, name: str, on_quit: Callable[[], None]):
        self._on_quit = on_quit
        self._status = "Idle"
        self._icon: Icon = self._create_icon(name)  # type: ignore[reportInvalidTypeForm]

    def _get_status_text(self, item) -> str:  # type: ignore[reportUnknownParameterType]
        return f"Status: {self._status}"

    def _create_icon(self, name: str) -> Icon:  # type: ignore[reportInvalidTypeForm]
        image = Image.new("RGB", (64, 64), "black")
        menu = Menu(
            MenuItem(self._get_status_text, None, enabled=False),
            Menu.SEPARATOR,
            MenuItem(
                "Settings",
                Menu(
                    MenuItem(f"Hotkey: {settings.HOTKEY}", None, enabled=False),
                    MenuItem(f"Model Size: {settings.MODEL_SIZE}", None, enabled=False),
                    MenuItem(
                        f"Compute Device: {settings.COMPUTE_DEVICE}",
                        None,
                        enabled=False,
                    ),
                ),
            ),
            Menu.SEPARATOR,
            MenuItem("Quit", self._on_quit_clicked),
        )
        return Icon(name, image, name, menu)

    def set_status(self, status: str):
        self._status = status
        self._icon.update_menu()

    def _on_quit_clicked(self) -> None:
        self.stop()
        self._on_quit()

    def start(self) -> None:
        """Starts the tray icon in a non-blocking way."""
        self._icon.run_detached()

    def stop(self) -> None:
        """Stops the tray icon and handles cleanup."""
        try:
            self._icon.stop()
        except AttributeError:
            # pystray may raise AttributeError during cleanup in some cases
            pass
