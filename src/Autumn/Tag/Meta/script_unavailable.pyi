from Autumn.Tag import AbstractTag
from Autumn.typing.types import TagChildren


class ScriptUnavailable(AbstractTag):

    def __init__(self,
                 *content: TagChildren): ...