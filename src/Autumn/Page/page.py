import threading
from typing import Literal, Any

from markupsafe import escape

from Autumn.Tag.Enums import Language
from Autumn.Tag.Meta import Title
from Autumn.Tag.abstract_tag import AbstractTag
from Autumn.Tag.Meta import Cdn
from Autumn.Tag.Meta import Head
from Autumn.abstract_base import AbstractBase


class Page(AbstractBase):
    """
    A page class representing an HTML document.
    """

    def __init__(self, name: str, /, *, direction: Literal["ltr", "rtl", "auto"] = "auto", language: Language | str = "en"):
        """
        Initializes a new page object.

        :param name: The name of the page.
        :param direction: The direction of the page.
        :param language: The language of the page.
        """
        self.name = name
        self.direction = direction
        self.language = language.value if isinstance(language, Language) else language
        self._tags: list[AbstractTag] = []
        self._requirements: list[Cdn] = []

        self._cache: list[str] = []

        self._lock = threading.Lock()

    def require(self, cdn: list[Cdn] | Cdn, /) -> "Page":
        """
        Requires CDN URL(s) for this specific page.

        :param cdn: The CDN URL(s).
        :return: This instance for chaining operations.
        """
        self._requirements.extend(cdn if isinstance(cdn, list) else [cdn])
        return self

    def tag(self, tag: list[AbstractTag] | AbstractTag, /) -> "Page":
        """
        Adds tag(s) to this page, which is often only a head and a body.

        :param tag: The tag(s) to add.
        :return: This instance for chaining operations.
        """
        self._tags.extend(tag if isinstance(tag, list) else [tag])
        return self

    def build(self, **build_kwargs: Any) -> str:
        """
        Builds this HTML page.

        :param build_kwargs: The kwargs to pass down the tree(these might be changed during the build,
            mostly by the child tag).
        :return: A string representing the HTML page.
        """

        dynamic = any(tag.dynamic for tag in self._tags)

        if not dynamic and self._cache:
            return self._cache[-1]

        self.before_build(**build_kwargs)

        head: Head | None = next(filter(lambda tag: isinstance(tag, Head), self._tags), None) # type: ignore

        if head is None:
            head = Head()
            self._tags.insert(0, head)

        with head._lock:
            head.tags.extend([Title(self.name), *self._requirements])

        out = ("<!DOCTYPE html>" +
                f'<html lang="{escape(self.language)}" dir="{escape(self.direction)}">' +
                "".join(tag.build(dynamic, **build_kwargs) for tag in self._tags) +
                "</html>")

        if not dynamic and not self._cache:
            self._cache.append(out)
        return out

    @property
    def dynamic(self) -> bool:
        """
        Returns whether this page is dynamic or not(checked via children's dynamic).

        :return: True if dynamic, False otherwise.
        """

        return any(tag.dynamic for tag in self._tags)
    @property
    def tags(self) -> list[AbstractTag]:
        """
        Returns a copy of the owning tags.

        :return: The copy.
        """
        return self._tags.copy()
    @property
    def requirements(self) -> list[Cdn]:
        """
        Returns a copy of the owning CDNs.

        :return: The copy.
        """

        return self._requirements.copy()