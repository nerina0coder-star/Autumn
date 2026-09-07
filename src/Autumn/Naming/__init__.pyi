from collections.abc import Callable
from typing import ClassVar

from .class_ import Class as Class
from .identifier import Identifier as Identifier
from .attribute_selector import AttributeSelector as AttributeSelector
from .name import Name as Name

def MakeSelector(
        state: Name | list[Name] | None = None,
        identifier: Identifier | list[Identifier] | None = None,
        cls: Class | list[Class] | None = None,
        selector: AttributeSelector | list[AttributeSelector] | None = None,
) -> str: ...

class Naming:
    MakeSelector: ClassVar[Callable[
        [
            Name | list[Name] | None,
            Identifier | list[Identifier] | None,
            Class | list[Class] | None,
            AttributeSelector | list[AttributeSelector] | None,
        ],
        str
    ]]

    Name: ClassVar[type[Name]]
    Identifier: ClassVar[type[Identifier]]
    Class: ClassVar[type[Class]]
    AttributeSelector: ClassVar[type[AttributeSelector]]
