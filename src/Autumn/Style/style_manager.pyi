import threading
from typing import Any

from Autumn.abstract_base import AbstractBase
from .abstract_style import AbstractStyle
from .sheet import Sheet
from .Styles import StyleHolder


class StyleManager(AbstractBase):

    Style: type[AbstractStyle]
    Sheet: type[Sheet]
    holder: type[StyleHolder]
    _styles: dict[str, AbstractStyle]
    _lock: threading.Lock

    def __init__(self) -> None: ...

    def register(self, name: str, template: AbstractStyle) -> None: ...

    def register_all(self, **data: AbstractStyle) -> StyleManager: ...

    def build(self, template_name: str, **build_kwargs: Any) -> str: ... # type: ignore