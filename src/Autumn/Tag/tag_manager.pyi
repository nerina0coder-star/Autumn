import threading
from collections.abc import Callable
from typing import Any

from .Meta import Meta
from .comment import Comment
from .abstract_tag import AbstractTag
from .Enums import Enums
from ..abstract_base import AbstractBase


class TagManager(AbstractBase):
    comment: type[Comment]
    meta: type[Meta]
    e: type[Enums]

    Tag: type[AbstractTag]

    _tags: dict[str, type[AbstractTag]]
    _aliases: dict[str, type[AbstractTag]]
    _lock: threading.Lock

    def __init__(self) -> None: ...

    def tag(self, tag: type[AbstractTag]) -> TagManager: ...

    def find(self, name: str) -> AbstractTag: ...

    def alias(self, name: str, result: type[AbstractTag]) -> type[AbstractTag]: ...

    def merge(self, other: TagManager) -> TagManager: ...

    def build(self, *, tag: AbstractTag, **kwargs: Any) -> str: ...  # type: ignore[override]

    def __getattr__(self, item: str) -> Callable[..., AbstractTag] | type[AbstractTag]: ...