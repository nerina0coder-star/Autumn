
from Autumn.Tag import AbstractTag
from Autumn.Tag.Enums import MimeType
from Autumn.Tag.Enums.Meta import LinkType, AsAttribute


class Link(AbstractTag):

    def __init__(self,
                 link: str,
                 link_type: LinkType | str | list[LinkType | str],
                 /, *,
                 as_: AsAttribute | None = None,
                 type_: MimeType | str | None = None): ...