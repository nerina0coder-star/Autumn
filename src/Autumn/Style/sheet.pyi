import threading
from typing import Any

from Autumn.Style.abstract_style import AbstractStyle
from Autumn.abstract_base import AbstractBase


class Sheet(AbstractBase):

    _caches: list[str]
    _lock: threading.Lock
    styles: list[AbstractStyle]

    def __init__(self, *styles: AbstractStyle) -> None: ...

    def build(self, cache_if_possible: bool = True, **kwargs: Any) -> str: ...