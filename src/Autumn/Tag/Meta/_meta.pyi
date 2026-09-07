from typing import Literal

from Autumn.Tag import AbstractTag


class Meta(AbstractTag):

    def __init__(self, *,
                 name: str | None = None,
                 content: list[str] | str | None = None,
                 charset: Literal["UTF-8"] | str | None = None,
                 sep: str = ","): ...