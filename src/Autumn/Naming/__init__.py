from .class_ import Class
from .identifier import Identifier
from .attribute_selector import AttributeSelector
from .name import Name

# --- Special Function ---

def MakeSelector(state = None,
                 identifier = None,
                 cls = None,
                 selector = None,):
    out = []

    if state is not None:
        if not isinstance(state, list):
            state = [state]
    else:
        state = []

    if identifier is not None:
        if not isinstance(identifier, list):
            identifier = [identifier]
    else:
        identifier = [identifier]

    if cls is not None:
        if not isinstance(cls, list):
            cls = [cls]
    else:
        cls = []

    if selector is not None:
        if not isinstance(selector, list):
            selector = [selector]
    else:
        selector = []

    mixed = [*state, *identifier, *cls, *selector]

    for i in mixed:
        adding = str(i) if not hasattr(i, "build") else i.build()
        out.append(f"{adding if len(out) == 1 else f",{adding}"}")

    return "".join(out)

# API

class Naming:
    """
    Naming - Contains classes used for naming.
    """

    MakeSelector = MakeSelector
    Name = Name
    Identifier = Identifier
    Class = Class
    AttributeSelector = AttributeSelector