from typing import ClassVar

from .as_attribute import AsAttribute as AsAttribute
from .link_type import LinkType as LinkType
from .script_type import ScriptType as ScriptType

class Meta:

    AsAttribute: ClassVar[type[AsAttribute]]
    ScriptType: ClassVar[type[ScriptType]]
    LinkType: ClassVar[type[LinkType]]
