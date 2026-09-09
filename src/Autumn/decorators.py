from collections.abc import Callable
from inspect import isroutine, isclass

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

    :param meth: The method that was decorated with no_lock.
    :return: The updated method.
    """
    if meth is None:
        return allow_lock  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify a method, given {meth}.")

    meth.__no_lock__ = False  # type: ignore[union-attr]
    return meth

def allow_unsafe(meth: T | None = None) -> T:
    """
    Allows unsafe method and will not wrap the method when doing ctrl.
    Note that this only works when it's used at class definition time,
    and that this won't work with __init__.

    :param meth: The method to decorate.
    :return: The decorated method.
    """
    if meth is None:
        return allow_unsafe  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify a method, given {meth}.")

    meth.__allow_unsafe__ = True  # type: ignore[union-attr]
    return meth

def make_safe(meth: T | None = None) -> T:
    """
    Nullifies the effect of allow_unsafe.
    Note that this only works when it's used at class definition time.

    :param meth: The method that was decorated with allow_unsafe.
    :return: The updated method.
    """

    if meth is None:
        return make_safe  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify a method, given {meth}.")

    meth.__allow_unsafe__ = False  # type: ignore[union-attr]
    return meth


def disable_autoinit(cls: T | None = None) -> T:
    """
    Nullifies the effect of parent's __children_autoinit__.

    :param meth: The method to decorate.
    :return: The decorated method.
    """
    if cls is None:
        return disable_autoinit   # type: ignore[return-value]
    if not isclass(cls):
        raise ValueError(f"Expected to modify a method, given {cls}.")

    cls.__autocall_init__ = False  # type: ignore[attr-defined]
    return cls


def lock(boolean: bool) -> Callable[[T | None], T]:
    """
    A shorthand. It true, it will allow locking, if false, it won't be locked.
    Note that this only works when it's used at class definition time.

    :param boolean: Whether this method should be locked.
    :return: A callable to decorate the method.
    """

    if boolean:
        return allow_lock
    else:
        return no_lock

def safe(boolean: bool) -> Callable[[T | None], T]:
    """
    A shorthand. If true, this method will stay safe as default and will be wrapped,
    if false, it won't be wrapped and it will remain unsafe.

    :param boolean: Whether this method should stay safe.
    :return: A callable to decorate the method.
    """

    if boolean:
        return make_safe
    else:
        return allow_unsafe

class Decorators:
    """
    Contains the decorators used in Autumn.
    """

    # noinspection PyTypeHints
    class Locking:
        no_lock: Callable[[T | None], T] = no_lock
        allow_lock: Callable[[T | None], T] = allow_lock
        lock: Callable[[bool], Callable[[T | None], T]] = lock

    # noinspection PyTypeHints
    class Safety:
        allow_unsafe: Callable[[T | None], T] = allow_unsafe
        make_safe: Callable[[T | None], T] = make_safe
        safe: Callable[[bool], Callable[[T | None], T]] = safe

    # noinspection PyTypeHints
    class Functionality:
        disable_autoinit: Callable[[T | None], T] = disable_autoinit
