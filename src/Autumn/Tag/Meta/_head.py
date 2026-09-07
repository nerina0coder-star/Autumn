from Autumn.Tag.abstract_tag import AbstractTag
from ._meta import Meta


class Head(AbstractTag):
    """
    Represents a Head tag in the document.
    """
    def __init__(self, *children):
        """
        Initializes a new instance.
        """
        self.name = "head"
        self.closable = True
        self.tags = [Meta(name="viewport", content=["width=device-width", "initial-scale=1.0"]),
                     Meta(charset="UTF-8")]
        self.tags.extend(dict.fromkeys(children))
        AbstractTag.__init__(self)