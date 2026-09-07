from typing import ClassVar

from ._cdn import Cdn as Cdn
from ._head import Head as Head
from ._link import Link as Link
from ._meta import Meta as MetaTag
from ._title import Title as Title
from ._script import Script as Script
from ._script_unavailable import ScriptUnavailable as ScriptUnavailable

class Meta:

    Cdn: ClassVar[type[Cdn]]
    Link: ClassVar[type[Link]]
    Script: ClassVar[type[Script]]
    Head: ClassVar[type[Head]]
    Meta: ClassVar[type[MetaTag]]
    Title: ClassVar[type[Title]]
    ScriptUnavailable: ClassVar[type[ScriptUnavailable]]