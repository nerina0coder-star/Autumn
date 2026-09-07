import threading

from Autumn.abstract_base import AbstractBase
from .abstract_style import AbstractStyle
from .sheet import Sheet
from .Styles import StyleHolder


class StyleManager(AbstractBase):
    """
    The class that helps manage the style objects.
    """

    def __init__(self):
        self.Style = AbstractStyle
        self.Sheet = Sheet

        self.holder = StyleHolder
        """
        Used to hold properties.
        """

        self._styles = {}
        """
        The dictionary of the style objects.
        """

        self._lock = threading.Lock()

    def register(self, name, template):
        with self._lock:
            self._styles[name] = template

    def register_all(self, **data):
        """
        Registers all the given styles.
        :param data: The styles to register.
        :return: Self
        """
        for k, v in data.items():
            self._styles[k] = v
        return self

    def build(self, template_name, **build_kwargs):
        with self._lock:
            return self._styles[template_name].build(True, **build_kwargs)
