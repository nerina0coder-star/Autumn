from typing import Literal, Any

from Autumn.Tag import AbstractTag
from Autumn.Tag.Enums.Meta import ScriptType


class Cdn(AbstractTag):

    link: str
    type: Literal["style", "script"]

    def __init__(self,
                 cdn_type: Literal["style", "script"],
                 link: str,
                 script_type: ScriptType | None = None,
                 **css_kwargs: Any
                 ) -> None: ...