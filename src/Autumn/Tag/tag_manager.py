import threading

from .Enums import Enums
from .Meta import Meta
from .abstract_tag import AbstractTag
from .comment import Comment
from ..abstract_base import AbstractBase


class TagManager(AbstractBase):
    """
    Manages the tags in Autumn independent of the class.
    """

    def __init__(self):
        """
        Creates a new instance of the Tag Manager.
        """
        self._tags = {}
        """
        Holds the tags in a dictionary for instant look-up.
        """

        self.meta = Meta
        self.e = Enums
        self.Tag = AbstractTag
        self.comment = Comment
        self._aliases = {}

        self._lock = threading.Lock()

    def tag(self, tag):
        """
        Adds a tag to the already-managed tags.
        :param tag: A tag with a Unique name.
        :return: This instance for chaining operations.
        """
        if (name := tag.__name__) not in self.tags:
            self._tags[name] = tag
        raise ValueError(f"Tag with name {name} already exists.")

    def find(self, name):
        """
        Finds a tag that's being managed.
        :param name: The name of the tag to find.
        :return: The found tag.
        """
        lst = next(filter(lambda tag: tag.startswith(name), self._tags.keys()), None)
        if lst is None:
            raise ValueError(f"Tag with name {name} does not exist.")
        return lst

    def alias(self, name, result):
        """
        Alias a tag to a name.
        Example:

        alias("p", Base.tag.content.Paragraph)

        Now you can simply do:

        Base.tag.p

        :param name: The name of the alias.
        :param result: The result of the alias.
        :return: The aliased result.
        """
        if name in self.__dict__ or name in dir(self) or name in self._aliases:
            raise ValueError(f"Alias or Real attribute with name {name} already exists in this instance.")
        self._aliases[name] = result
        return result

    def merge(self, other):
        """
        Merges the given tag manager with the other, resulting in an update in this manager.
        :param other: Another tag manager.
        :return: Self.
        """

        with other._lock:
            self._aliases.update(other._aliases)
            self._tags.update(other._tags)

        return self

    def build(self, *, tag: AbstractTag, **kwargs) -> str:
        """
        Another way to write tag.build()
        :param tag: A tag.
        :return: The built tag.
        """
        self.before_build(tag=tag)
        return tag.build(**kwargs)

    def __getattr__(self, name): # Used for making aliases work.
        if name in self._aliases:
            return self._aliases[name]
        raise AttributeError(f"Tag with name {name} does not exist")