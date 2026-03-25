"""Type stubs for loguru module."""

from typing import Any, Callable, Optional, Protocol
from contextlib import contextmanager

class Logger:
    """Loguru logger instance with structured logging methods."""

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def info(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def critical(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def exception(self, message: str, *args: Any, **kwargs: Any) -> None: ...
    def add(
        self,
        sink: Any,
        *,
        format: Optional[str] = None,
        level: str = "DEBUG",
        colorize: Optional[bool] = None,
        serialize: bool = False,
        backtrace: bool = True,
        diagnose: bool = True,
        **kwargs: Any,
    ) -> int: ...
    def remove(self, handler_id: Optional[int] = None) -> None: ...
    def enable(self, name: str) -> None: ...
    def disable(self, name: str) -> None: ...
    @contextmanager
    def catch(
        self,
        exception: type[BaseException] | tuple[type[BaseException], ...] = ...,
        *,
        level: str = "ERROR",
        reraise: bool = False,
        **kwargs: Any,
    ): ...

logger: Logger
