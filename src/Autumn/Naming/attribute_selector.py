import threading

from markupsafe import escape

from Autumn.abstract_base import AbstractBase


class AttributeSelector(AbstractBase):

    def __init__(self, attr, value):
        self._attr = attr
        self._value = value

        self._lock = threading.Lock()

    def build(self, **kwargs) -> str:
        with self._lock:
            self.before_build(**kwargs)
            return f'[{escape(self._attr)}="{escape(self._attr)}"]'