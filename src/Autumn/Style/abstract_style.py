import threading

from Autumn.Style.Styles import StyleHolder
from Autumn.abstract_base import AbstractBase


class AbstractStyle(AbstractBase):
    """
    The base style class that build styles like:

    class-name {
        color: red;
    }

    Note on self.name: This is the tag name we apply the styles on,
    to also apply it on its identifier and classes, set self.identifier to its identifier
    and self.classes to its classes.
    """

    __no_new__ = True

    def __init__(self):

        if getattr(self, "name", None) is None:
            self.name = []
        if getattr(self, "identifier", None) is None:
            self.identifier = []
        if getattr(self, "classes", None) is None:
            self.classes = []
        if not (hasattr(self, "styles") and isinstance(self.styles, list)):
            self.styles = []
        if not (hasattr(self, "dynamic") and isinstance(self.dynamic, bool)):
            self.dynamic = False
        if not (hasattr(self, "_cache") and isinstance(self._cache, list)):
            self._cache = []

        if not isinstance(self.name, list):
            self.name = [self.name] # type: Ignore

        self._lock = threading.RLock()

        # Please note that this is because user's code is unpredictable, therefore using RLock's flexibility
        # is REQUIRED. Even I consider RLock a code smell, but in this case, it cannot be helped.



    def build(self, cache_if_possible = True, **kwargs):
        """
        Builds the style.
        :param cache_if_possible: If true, the style is cached if this style is not dynamic.
        :param kwargs: The kwargs to pass to all sub-style holders.
        :return:
        """ # TODO add at rules support
        if not self.dynamic and self._cache:
            return self._cache[-1]

        if (result := self.before_build(**kwargs)) is not None:
            if not self._cache and not self.dynamic and cache_if_possible:
                self._cache.append(result)
            return result

        out = []

        if self.name:
            out.extend([name if isinstance(name, str) else name.build(**kwargs) for name in self.name])
        if self.classes:
            out.extend([cls if isinstance(cls, str) else f".{str(cls)}" for cls in self.classes])
        if self.identifier:
            out.append(self.identifier if isinstance(self.identifier, str) else f"#{str(self.identifier)}")

        out.append("{")

        if self.styles:
            for style in self.styles:
                out.append(style.build(**kwargs) if isinstance(style, StyleHolder) else style)


        out.append("}")

        if not self._cache and not self.dynamic and cache_if_possible:
            self._cache.append(out)

        return "".join(out)