from collections.abc import Callable
from functools import wraps
from inspect import isroutine, isclass
from typing import Any, TypeVar

T = TypeVar('T')


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


def disable_autoinit(meth: T | None = None) -> T:
    """
    Nullifies the effect of parent's __children_autoinit__.

    :param meth: The method to decorate.
    :return: The decorated method.
    """
    if meth is None:
        return disable_autoinit  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify __init__, given {meth}.")

    meth.__no_autoinit__ = True  # type: ignore[union-attr]
    return meth


def enable_autoinit(meth: T | None = None) -> T:
    """
    Nullifies the effect of disable_autoinit.

    :param meth: The method that was decorated with disable_autoinit.
    :return: The changed method.
    """

    if meth is None:
        return enable_autoinit  # type: ignore[return-value]
    if not isroutine(meth):
        raise ValueError(f"Expected to modify __init__, given {meth}.")

    meth.__no_autoinit__ = False  # type: ignore[union-attr]
    return meth


def only_self(cls: T | None = None) -> T:
    """
    Used for auto init. Changes the default argument of children to "self".

    :param cls: The class to decorate.
    :return: The decorated class.
    """

    if cls is None:
        return only_self  # type: ignore[return-value]
    if not isclass(cls):
        raise ValueError(f"expected to modify a class, given {cls}")

    before = getattr(cls.__init_subclass__, "__func__")

    @wraps(before)
    def init_subclass(cls2: Any, **kwargs: Any) -> None:
        before(cls2, **kwargs)  # type: ignore[unused-ignore]
        if not hasattr(cls2, "__params_to_parent__"):
            setattr(cls2, "__params_to_parent__", (lambda self, *args, **kws: (tuple(), dict())))

    setattr(cls, "__init_subclass__", classmethod(init_subclass))  # type: ignore[arg-type]

    return cls


def use_as_hook(cls: None | T = None, /, *, name: str = "__init__") -> Callable[[T], T] | T:
    """
    Extracts the given function name and uses at `__init_hook__`.

    :param name: The name of the function.
    :param cls: If cls is None, it will proceed normally, returning a function/callable.
        If not, it will call the method to be returned and returns the class.
    :return: A callable that takes a class and returns it. Or the given cls.
    """

    if type(name) is not str:
        raise ValueError(f"Expected str, but given {name}")

    def meth(cls: T) -> T:

        if not isclass(cls):
            raise ValueError(f"Expected a class, but given {cls}")

        setattr(cls, "__init_hook__", getattr(cls, name))

        return cls

    if cls is not None:
        return meth(cls)

    return meth


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


def autoinit(boolean: bool) -> Callable[[T | None], T]:
    """
    A shorthand. If true, this __init__ will sign the class as `auto init`-following(parent's influence counts).
    If false, this will sign the class as `auto init`-ignoring.

    :param boolean: Whether this method should remain `auto init` following or not.
    :return: The method to wrap this __init__.
    """

    if boolean:
        return enable_autoinit
    else:
        return disable_autoinit


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
    class AutoInit:
        disable_autoinit: Callable[[T | None], T] = disable_autoinit
        enable_autoinit: Callable[[T | None], T] = enable_autoinit
        only_self: Callable[[T | None], T] = only_self
        use_as_hook: Callable[[str], Callable[[T], T]] = use_as_hook
        autoinit: Callable[[bool], Callable[[T | None], T]] = autoinit
