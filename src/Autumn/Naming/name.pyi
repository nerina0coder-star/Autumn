import threading
from typing import Any

from Autumn.Naming import Identifier, Class
from Autumn.Tag.abstract_tag import AbstractTag
from Autumn.abstract_base import AbstractBase


class Name(AbstractBase):

    name: str
    identifier: Identifier
    classes: list[Class]
    attrs: dict[str, str]
    _lock: threading.Lock
    _cache: list[str]

    def __init__(self,
                 name: str,
                 id_: Identifier,
                 classes: list[Class],
                 /, *,
                 attributes: dict[str, str] | None = None,
                 ) -> None: ...

    def build(self,
              cache_if_possible: bool = True,
              **kwargs: Any
              ) -> str: ...

    @staticmethod
    def from_tag(tag: AbstractTag) -> Name: ...