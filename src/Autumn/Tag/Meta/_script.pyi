from Autumn.Tag import AbstractTag
from Autumn.Tag.Enums.Meta import ScriptType


class Script(AbstractTag):

    def __init__(self,
                 src: str,
                 type_: ScriptType = ScriptType.JS,
                 /): ...