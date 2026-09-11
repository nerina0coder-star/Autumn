from Autumn.Tag.abstract_tag import AbstractTag


class ScriptUnavailable(AbstractTag):
    """
    A meta tag that contains the view to show to the users
    with old browsers where Script/Modern script is unavailable.
    """
    def __init__(self, *content):
        self.tags = list(content)
        self.name = "noscript"
        self.closable = True
        AbstractTag.__init__(self)
