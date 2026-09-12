import threading
from typing import Any
from collections.abc import Callable

from Autumn.Naming import Identifier, Class
from Autumn.abstract_base import AbstractBase
from Autumn.typing.types import T


class AbstractTag(AbstractBase):
    type _comparison = AbstractTag | int | float
    type _add_return = AbstractTag | list[AbstractTag] | set[AbstractTag] | dict[int, AbstractTag] | tuple[AbstractTag]
    __hash__ = object.__hash__

    _lock: threading.RLock
    _reverse_addition: bool
    _mock_cls: type[AbstractTag] | None

    tags: list[AbstractTag | str]
    identifier: Identifier | None
    classes: list[Class]
    dynamic: bool
    _cache: list[str]
    worth: int | float
    name: str
    attributes: dict[str, Any]
    closable: bool
    preferred_parent: Callable[[], AbstractTag | list[Any] | set[Any] | dict[Any, Any] | tuple[Any]]

    def __init__(self) -> None: ...

    def identifiers(self) -> list[Identifier]: ...

    def duplicate_identifiers(self) -> list[Identifier]: ...

    def delete_cache(self) -> int: ...

    def build(self, cache_if_possible: bool = True, **kwargs: Any) -> str: ...

    def _new(self) -> AbstractTag: ...

    def __mul__(self: T, other: int) -> T: ...

    def __rmul__(self: T, other: int) -> T: ...

    def __add__(self, other: AbstractTag | list[AbstractTag]) -> _add_return: ...

    def __radd__(self, other: AbstractTag | list[AbstractTag]) -> _add_return: ...

    def __lshift__(self, other: AbstractTag | str) -> AbstractTag: ...

    def __rrshift__(self, other: AbstractTag | str) -> AbstractTag: ...

    def __rshift__(self, other: AbstractTag) -> AbstractTag: ...

    def __sub__(self, other: type[AbstractTag] | list[type[AbstractTag]]) -> AbstractTag: ...

    def __eq__(self, other: _comparison) -> bool: ... # type: ignore

    def __ne__(self, other: _comparison) -> bool: ... # type: ignore

    def __lt__(self, other: _comparison) -> bool: ...

    def __gt__(self, other: _comparison) -> bool: ...

    def __le__(self, other: _comparison) -> bool: ...

    def __ge__(self, other: _comparison) -> bool: ...

    def __contains__(self, item: object | str | AbstractTag | type[AbstractTag]) -> bool: ...

    def _resolve_parent(self, lst: list[AbstractTag]) -> AbstractTag | list[AbstractTag] | set[AbstractTag] | tuple[AbstractTag] | dict[int, AbstractTag]: ...

    def _shared_plus(self, other: AbstractTag | list[AbstractTag]) -> _add_return: ...
