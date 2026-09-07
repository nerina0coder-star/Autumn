import threading

from Autumn.Style.abstract_style import AbstractStyle
from Autumn.abstract_base import AbstractBase


class Sheet(AbstractBase):
    """
    Sheet contains all styles made, so they will be made by just one build call.
    """

    def __init__(self, *styles: AbstractStyle):
        self.styles = list(styles)
        self._caches = []
        self._lock = threading.Lock()

    def build(self, cache_if_possible: bool = True, **kwargs) -> str:
        static = not any(style.dynamic for style in self.styles)

        if static and self._caches:
            return self._caches[-1]

        if (result := self.before_build(**kwargs)) is not None:
            out = result
        else:
            out = "".join(i.build() for i in self.styles)

        if static and cache_if_possible and not self._caches:
            self._caches.append(out)

        return out