import abc
import threading
from typing import Any

from markupsafe import Markup

from Autumn.abstract_base import AbstractBase


class StyleHolder(AbstractBase, abc.ABC):

    _lock: threading.RLock
    _cache: list[str]

    name: str
    value: str | Markup
    important: bool
    dynamic: bool

    def __init__(self) -> None: ...

    def build(self, **kwargs: Any) -> str: ...