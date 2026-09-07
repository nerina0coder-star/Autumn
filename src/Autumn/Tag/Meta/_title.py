from Autumn.Tag.abstract_tag import AbstractTag


class Title(AbstractTag):
    """
    Represents a title(The name of the document).
    """

    def __init__(self, title, /):
        self.name = "title"
        self.closable = True
        self.tags = [title]

        AbstractTag.__init__(self)