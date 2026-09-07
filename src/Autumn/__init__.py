"""
Autumn - A framework for serverside HTML rendering.

Autumn is an exceptional framework built for speed and developer's experience.
This framework is primary Object-Oriented, and cannot
be used as functional.

The framework starts with the "new" function(available in this package)
and the entire project is loaded after loading the base.

When defining tags, pay close attention to it.

See whether the function is dynamic(The
behavior changes after each generation during the current runtime) or static(one output can be used for infinitely more
generations during the current runtime).

Then change the dynamic attribute/content/etc... of your tag as needed.
"""

from .base import Base, current_base
from .abstract_base import AbstractBase

def new() -> Base:
    """
    Returns a new Base instance.
    :return: a Base class.
    """
    return Base()

__all__ = ["new", "Base", "current_base", "AbstractBase"]
