import abc
import threading
from typing import Any

from Autumn.Naming import Name, Class
from Autumn.Naming.identifier import Identifier
from Autumn.Style.Styles.style_holder import StyleHolder
from Autumn.abstract_base import AbstractBase


class AbstractStyle(AbstractBase, abc.ABC):

    name: list[Name | str]
    identifier: list[Identifier | str]
    classes: list[Class | str]
    styles: list[StyleHolder | str]
    dynamic: bool
    _cache: list[str]
    _lock: threading.RLock

    def __init__(self) -> None: ...

    def build(self, cache_if_possible: bool = True, **kwargs: Any) -> str: ...

