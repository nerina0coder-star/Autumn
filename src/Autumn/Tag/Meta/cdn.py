from Autumn.Tag.Enums.Meta import LinkType
from Autumn.Tag.abstract_tag import AbstractTag
from .link import Link
from .script import Script


class Cdn(AbstractTag):
    """
    Represents a CDN that links the assets from the CDN to the document.
    """

    def __init__(self, cdn_type, link,
                 /, *, script_type = None, **css_kwargs):
        """
        Initializes a new instance of the Cdn tag.

        :param cdn_type: The type of the CDN.
        :param link: The link to the CDN.
        :param script_type: Used for Script, the type of the script.
        :param css_kwargs: The arguments to give the Link(if type is style).
        """
        self.type = cdn_type
        self.link = link
        """
        Contains the given link.
        """

        self.script_type = script_type
        self.ck = css_kwargs
        AbstractTag.__init__(self)

    def before_build(self, **kwargs):
        return Link(self.link, LinkType.STYLESHEET, **self.ck).build(**kwargs) if self.type == "style" else Script(self.link, self.script_type).build(**kwargs)