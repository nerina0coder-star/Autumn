import threading

from markupsafe import escape, Markup

from Autumn.abstract_base import AbstractBase


class StyleHolder(AbstractBase):
    """
    Holds all styles.
    Be careful that in this special case, dynamic is True.
    """

    __no_new__ = True

    def __init__(self):
        self._lock = threading.RLock()

        # Please note that this is because user's code is unpredictable, therefore using RLock's flexibility
        # is REQUIRED. Even I consider RLock a code smell, but in this case, it cannot be helped.

        if not (hasattr(self, 'name') and isinstance(self.name, str)):
            self.name = ""
        if not (hasattr(self, "value") and isinstance(self.value, str)):
            self.value = ""

        if not (hasattr(self, "important") and isinstance(self.important, bool)):
            self.important = False

        if not (hasattr(self, "dynamic") and isinstance(self.dynamic, bool)):
            self.dynamic = True

        self._cache = []

    def build(self, **kwargs):
        if not self.dynamic and self._cache:
            return self._cache[-1]

        if (result := self.before_build(**kwargs)) is not None:
            if not self._cache and not self.dynamic:
                self._cache.append(result)
            return result

        value = self.value
        if self.value.startswith('"') and self.value.endswith('"') \
                or self.value.startswith("'") and self.value.endswith("'"):
            value = Markup(self.value[0]) + escape(self.value[1:-2]) + Markup(self.value[-1])

        out = f"{self.name}:{escape(value)}{f"!important" if self.important else ""};"

        if not self._cache and not self.dynamic:
            self._cache.append(out)

        return out

        # Even tho markup safe's escape is used only for HTML, it's also useful for escaping ""''<>, which are NOT used in normal CSS.