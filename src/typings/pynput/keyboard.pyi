"""Type stubs for pynput.keyboard module."""

from typing import Any, Callable, ContextManager, Optional, Union

class Key:
    """Enumeration of special keys."""

    shift: Key
    shift_r: Key
    ctrl: Key
    ctrl_r: Key
    alt: Key
    alt_r: Key
    f1: Key
    f2: Key
    f3: Key
    f4: Key
    f5: Key
    f6: Key
    f7: Key
    f8: Key
    f9: Key
    f10: Key
    f11: Key
    f12: Key
    backspace: Key
    tab: Key
    enter: Key
    caps_lock: Key
    esc: Key
    space: Key
    page_up: Key
    page_down: Key
    end: Key
    home: Key
    left: Key
    up: Key
    right: Key
    down: Key
    insert: Key
    delete: Key
    a: Key
    b: Key
    c: Key
    d: Key
    e: Key
    f: Key
    g: Key
    h: Key
    i: Key
    j: Key
    k: Key
    l: Key
    m: Key
    n: Key
    o: Key
    p: Key
    q: Key
    r: Key
    s: Key
    t: Key
    u: Key
    v: Key
    w: Key
    x: Key
    y: Key
    z: Key
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class KeyCode:
    """Represents a key code."""

    vk: Optional[int]
    char: Optional[str]

    def __init__(
        self, *, vk: Optional[int] = None, char: Optional[str] = None
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class Controller:
    """Simulates keyboard input."""

    def type(self, string: str) -> None: ...
    def press(self, key: Union[Key, KeyCode, str]) -> None: ...
    def release(self, key: Union[Key, KeyCode, str]) -> None: ...
    def pressed(self, *keys: Union[Key, KeyCode, str]) -> ContextManager[Any]: ...

class Listener:
    """Listens for keyboard events."""

    def __init__(
        self,
        on_press: Optional[Callable[[Union[Key, KeyCode]], None]] = None,
        on_release: Optional[Callable[[Union[Key, KeyCode]], None]] = None,
    ) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def join(self, timeout: Optional[float] = None) -> bool: ...
    def is_alive(self) -> bool: ...
