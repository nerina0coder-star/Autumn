from collections.abc import Callable
from inspect import isroutine

from Autumn.typing.types import T


def no_lock(meth: T | None = None) -> T:
    """
    Indicates this function should not be locked.
    Note that this only works when it's used at class definition time.

    :param meth: The method to decorate.
    :return: The decorated function.
    """
    if meth is None:
        return no_lock  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify a method, given {meth}.")

    meth.__no_lock__ = True  # type: ignore[union-attr]
    return meth

def allow_lock(meth: T | None = None) -> T:
    """
    Nullifies the effect of no_lock.
    Note that this only works when it's used at class definition time.

    :param meth: The method to that was wrapped with no_lock.
    :return: The updated method.
    """
    if meth is None:
        return allow_lock  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify a method, given {meth}.")

    meth.__no_lock__ = False  # type: ignore[union-attr]
    return meth

def lock(boolean: bool) -> Callable[[T | None], T]:
    """
    A shorthand. It true, it will allow locking, if false, it won't be locked.
    Note that this only works when it's used at class definition time.

    :param boolean: Whether this method should be locked.
    :return: A callable to wrap the method.
    """

    if boolean:
        return allow_lock
    else:
        return no_lock

class Decorators:
    """
    Contains the decorators used in Autumn.
    """

    no_lock: Callable[[T | None], T] = no_lock
    allow_lock: Callable[[T | None], T] = allow_lock
    lock: Callable[[bool], Callable[[T | None], T]] = lock
