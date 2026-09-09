from Autumn.Tag import AbstractTag
from Autumn.typing.types import TagChildren


class Head(AbstractTag):

    def __init__(self,
                 *children: TagChildren): ...