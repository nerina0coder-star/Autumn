from Autumn.Tag.abstract_tag import AbstractTag
from Autumn.Tag.Enums.Meta import ScriptType


class Script(AbstractTag):
    """
    Represents a Script tag.
    """

    def __init__(
            self,
            src,
            type_ = ScriptType.JS,
            /):
        """
        Initializes a new instance.

        :param src: The link to the source of the script.
        :param type_: The type of the script.
        """
        self.attributes = {
            "src": src,
            "type": type_,
        }
        self.name = "script"
        self.closable = True
        AbstractTag.__init__(self)