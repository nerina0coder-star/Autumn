from typing import Any

from markupsafe import escape, Markup

from Autumn.Tag.abstract_tag import AbstractTag


class Comment(AbstractTag):
    """
    Represents an HTML comment, also seen as <!-- Content -->
    """
    def __init__(self, message: str, /):
        self.message = message
        self.name = "comment"
        AbstractTag.__init__(self)

    def build(self, cache_if_possible: bool = True, **kwargs: Any) -> str:
        if type(self) != Comment:
            raise TypeError("Cannot inherit from comment")
        if self._cache:
            return self._cache[-1]

        self.before_build(**kwargs)

        out = Markup("<!-- ") + escape(self.message) + Markup(" -->")
        self._cache.append(out)
        return out