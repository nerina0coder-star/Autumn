import copy
import threading

from markupsafe import escape

from Autumn.abstract_base import AbstractBase


class Name(AbstractBase):
    """
    Represents a CSS name.
    """

    def __init__(self,
                 name,
                 id_,
                 classes,
                 /, *,
                 attributes = None):
        """
        :param attributes: CSS/JS only
        """
        self.name = name
        self.identifier = id_
        self.classes = classes

        self.attrs = attributes

        self._lock = threading.Lock()

        self._cache = []

    def build(self, cache_if_possible = True, **kwargs):

        out = [self.name]

        self.before_build(**kwargs)

        if self.identifier:
            out.append(f"#{self.identifier}")

        if self.classes:
            for cls in self.classes:
                out.append(f".{cls}")

        if self.attrs:
            for k, v in self.attrs.items():
                out.append(f'[{escape(k)}="{escape(v)}"]')

        return ''.join(out)

    @staticmethod
    def from_tag(tag):
        return Name(tag.name, tag.identifier, copy.deepcopy(tag.classes))