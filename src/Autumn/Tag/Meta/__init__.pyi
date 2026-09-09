from typing import ClassVar

from .cdn import Cdn as Cdn
from .head import Head as Head
from .link import Link as Link
from .meta import Meta as MetaTag
from .title import Title as Title
from .script import Script as Script
from .script_unavailable import ScriptUnavailable as ScriptUnavailable

class Meta:

    Cdn: ClassVar[type[Cdn]]
    Link: ClassVar[type[Link]]
    Script: ClassVar[type[Script]]
    Head: ClassVar[type[Head]]
    Meta: ClassVar[type[MetaTag]]
    Title: ClassVar[type[Title]]
    ScriptUnavailable: ClassVar[type[ScriptUnavailable]]