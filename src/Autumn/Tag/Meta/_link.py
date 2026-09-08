from collections.abc import Iterable

from Autumn.Tag.Enums.Meta import LinkType
from Autumn.Tag.abstract_tag import AbstractTag


class Link(AbstractTag):
    """
    Represents a link to another route or website.
    """
    def __init__(self, link,
                 link_type,
                 /, *,
                 as_ = None,
                 type_ = None):
        """
        Initializes a new instance.

        :param link: The link (str) to the website.
        :param link_type: The type of the link.
        :param as_: Used in mapping.
        :param type_: The MimeType.
        """
        self.attributes = {
            "href": link,
            "rel": ""
        }
        self.name = "link"

        rel = []

        for lnk in ([None] if link_type is None else link_type if isinstance(link_type, Iterable) else [link_type]):
            if lnk is None:
                raise ValueError("link_type must be not-None, specifically, a LinkType/string or list of LinkTypes/strings.")

            if len(rel) != 0:
                rel.append(" ")
            rel.append(f"{lnk.value if isinstance(lnk, LinkType) else lnk}")

        self.attributes["rel"] = "".join(rel)

        if as_:
            self.attributes["as"] = as_.value
        if type_:
            self.attributes["type"] = type_

        AbstractTag.__init__(self)