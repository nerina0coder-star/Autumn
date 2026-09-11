import threading
from typing import Any

from .page import Page
from ..Tag.Meta import Cdn
from ..abstract_base import AbstractBase


class PageManager(AbstractBase):
    """
    A page manager for managing multiple pages.
    """

    def __init__(self, cdn: list[Cdn] | Cdn, /):
        """
        Initializes a new PageManager instance.

        :param cdn: The CDNs to include in all pages.
        """
        self._cdn: list[Cdn] = cdn if isinstance(cdn, list) else [cdn]
        self._caches: dict[str, str] = {}
        self._pages: dict[str, Page] = {}

        self._lock = threading.Lock()

    def require(self, cdn: list[Cdn] | Cdn, /) -> "PageManager":
        """
        Adds a new CDN to all pages being managed.

        :param cdn: The CDN(s) to include in all pages.
        :return: This instance for chaining operations.
        """
        self._cdn.extend(c for c in (cdn if isinstance(cdn, list) else [cdn]) if c not in self._cdn)
        return self

    def new(self, name: str, /) -> Page:
        """
        Adds a new page to the pages being managed.

        :param name: The name of the page to add, must be unique.
        :return: The newly created page.
        """
        page = Page(name)
        page.requirements.extend(self._cdn)
        if not name in self._pages:
            self._pages[name] = page
            return page
        raise ValueError("Page already exists.")

    def register(self, page: Page, /) -> Page:
        """
        Adds a new page to the pages being managed.

        :param page: The new page to add.
        :return: The page that was added.
        """
        if not all(cdn in page.requirements for cdn in self._cdn):
            page.require([cdn for cdn in self._cdn if cdn not in page.requirements])
        if not (name := page.name) in self._pages:
            self._pages[name] = page
            return page
        raise ValueError("Page already exists.")

    def build(self, name: str, **build_kwargs) -> str: # type: ignore
        """
        Builds a managed page, and caches non-dynamic pages.

        :param name: The name of the page.
        :return: The built page(HTML).
        """
        page = self._pages[name]
        if page.dynamic:
            return page.build(**build_kwargs)

        out = page.build(**build_kwargs)

        if name not in self._caches and not page.dynamic:
            self._caches[name] = out
        return out

    def merge(self, other: "PageManager") -> "PageManager":
        """
        Merges the given page manager with self, modifying the current page manager.

        :param other: Another page manager.
        :return: Self.
        """

        self._cdn.extend(other._cdn)
        self._pages.update(other._pages)
        self._caches.update(other._caches)

        return self

    @property
    def pages(self) -> dict[str, Page]:
        """
        Returns a copy of all the pages.

        :return: The copy.
        """
        return self._pages.copy()

    @pages.setter
    def pages(self, value: Any) -> None:
        """
        Raises AttributeError.

        :param value: Anything.
        :raises AttributeError: Can't update pages.
        """
        raise AttributeError("Can't update pages.")

    @pages.deleter
    def pages(self) -> None:
        """
        Raises AttributeError.

        :raises AttributeError: Can't delete pages.
        """

        raise AttributeError("Can't delete pages.")

    @property
    def caches(self) -> dict[str, str]:
        """
        Returns a copy of all the caches.

        :return: The copy.
        """

        return self._caches

    @caches.setter
    def caches(self, value: Any) -> None:
        """
        Raises AttributeError.

        :param value: Anything.
        :raises AttributeError: Can't update caches.
        """

        raise AttributeError("Can't update caches.")

    @caches.deleter
    def caches(self) -> None:
        """
        Raises AttributeError.

        :raises AttributeError: Can't delete caches.
        """

        raise AttributeError("Can't delete caches.")

    @property
    def Page(self) -> type[Page]:
        """
        Returns a page class to prevent importing it.
        """

        return Page