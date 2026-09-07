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
        if (not isinstance(content, Iterable) or isinstance(content, str)) and content is not None:
            content = [content]

        self.name = "meta"
        self.attributes = {
            "name": name,
            "content": content[0] + "".join(f"{sep}{cnt}"for cnt in content[1:]),
        } if name and content else {"charset": charset} if charset else None

        if self.attributes is None:
            raise ValueError("Expected name and content, or charset, to be given")

        AbstractTag.__init__(self)