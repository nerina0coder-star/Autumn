import threading
from types import TracebackType
from typing import Any, Literal

from Autumn import Decorators
from Autumn.Naming import Naming
from Autumn.Page import PageManager
from Autumn.Style import StyleManager
from Autumn.Tag import TagManager
from Autumn.typing.types import T



current_base: Base


class Base:

    page: PageManager
    tag: TagManager
    style: StyleManager
    name: type[Naming]

    decorators: type[Decorators]

    _wrapped: list[Any]

    _lock: threading.Lock
    _extensions: list[Any]

    @property
    def extensions(self) -> list[Any]: ...

    @extensions.setter
    def extensions(self, value: Any) -> None: ...

    @extensions.deleter
    def extensions(self) -> None: ...

    @property
    def wrapped(self) -> list[Any]: ...

    @wrapped.setter
    def wrapped(self, value: type[Any]) -> None: ...

    @wrapped.deleter
    def wrapped(self) -> None: ...

    def read(self, attribute: Literal["extensions", "wrapped"], function: str, *args: Any, **kwargs: Any) -> Any: ...

    def write(self, attribute: Literal["extensions", "wrapped"], function: str, *args: Any, **kwargs: Any) -> Any: ...

    def ctrl(self, cls: type[T] | None = None) -> type[T]: ...

    def __enter__(self) -> None: ...

    def __exit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None: ...

    def this(self) -> Base: ...

    def merge_new(self, other: Base) -> Base: ...

    @classmethod
    def merge(cls, one: Base, two: Base) -> Base: ...

    def own(self, cls: Any) -> None: ...

    def _notify_extensions_of_exception(self, **kwargs: Any) -> None: ...
