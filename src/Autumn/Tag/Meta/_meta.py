from collections.abc import Iterable

from Autumn.Tag.abstract_tag import AbstractTag


class Meta(AbstractTag):
    """
    Contains metadata about the document.
    """

    def __init__(self, *,
                 name = None,
                 content = None,
                 charset = None,
                 sep = ","):
        """
        Constructs a new Meta object, used to contain metadata about the document.

        :param name: The name of the metadata, e.g., CSRF. Should be used with content.
        :param content: The content of the metadata, e.g., token. Should be used with name.
        :param charset: Used when creating a metadata that defines the charset.
            When using this, name and content must be empty.
        :param sep: A separator for the content of the metadata.
        """

        if (not isinstance(content, Iterable) or isinstance(content, str)) and content is not None:
            content = [content]

        self.name = "meta"
        self.attributes = {  # type: ignore[assignment]
            "name": name,
            "content": content[0] + "".join(f"{sep}{cnt}"for cnt in content[1:]),
        } if name and content else {"charset": charset} if charset else None

        if self.attributes is None:
            raise ValueError("Expected name and content, or charset, to be given")

        AbstractTag.__init__(self)