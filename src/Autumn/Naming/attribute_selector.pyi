import threading
from typing import Any

from Autumn.abstract_base import AbstractBase


class AttributeSelector(AbstractBase):

    _lock: threading.Lock
    _attr: str
    _value: str

    def __init__(self, attr: str, value: str): ...

    def build(self, **kwargs: Any) -> str: ...