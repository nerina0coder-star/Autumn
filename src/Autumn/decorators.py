from collections.abc import Callable
from typing import Any


def no_lock(meth: Callable[..., Any] | None = None) -> Callable[..., Any]:
    """
    Indicates this function should not be locked.
    Note that this only works when it's used at class definition time.

    :param meth: The method to decorate.
    :return: The decorated function.
    """
    if meth is None:
        return no_lock

    meth.__no_lock__ = True  # type: ignore[attr-defined]
    return meth

def allow_lock(meth: Callable[..., Any] | None = None) -> Callable[..., Any]:
    """
    Nullifies the effect of no_lock.
    Note that this only works when it's used at class definition time.

    :param meth: The method to that was wrapped with no_lock.
    :return: The updated method.
    """
    if meth is None:
        return allow_lock

    meth.__no_lock__ = False  # type: ignore[attr-defined]
    return meth

class Decorators:
    """
    Contains the decorators used in Autumn.
    """

    no_lock: Callable[[Callable[..., Any] | None], Callable[..., Any]] = no_lock
    allow_lock: Callable[[Callable[..., Any] | None], Callable[..., Any]] = allow_lock
