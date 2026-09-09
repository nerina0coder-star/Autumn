import abc
import copy
import threading
from collections.abc import Callable
from functools import wraps
from inspect import signature, isroutine
from typing import Any


class AbstractBase(abc.ABC):
    """
    The base of most, if not all, of classes in Autumn.
    """

    @classmethod
    def __handle_no_new__(cls) -> None:
        """
        (Internal handler) Injects no new.
        """
        if cls.__dict__.get("__no_new__", False):

            def new(cls2: type, *__: Any, **___: Any) -> Any:
                if cls2 is cls:
                    raise RuntimeError(f"Cannot create class {cls.__name__}, class declared "
                                    "No New.")
                return super().__new__(cls2)  # type: ignore[misc]

            cls.__new__ = new  # type: ignore[method-assign,assignment]

    @classmethod
    def __handle_locking__(cls) -> None:
        """
        (Internal handler) Injects auto-locking.
        """
        for k, v in cls.__dict__.items():

            if not (isroutine(v) and (not k.startswith("_") or k.startswith("__"))):
                continue

            if isinstance(v, staticmethod):
                continue

            if hasattr(v, "__no_lock__") and v.__no_lock__:
                continue

            if k in [
                "__getattribute__",
                "__setattr__",
                "__del__",
                "__init__",
                "__new__",
                "__init_subclass__",
            ]:
                continue

            items = [
                "__name__",
                "__doc__",
                "__str__",
                "__qualname__",
                "__module__",
                "__annotations__",
                "__type_params__"
            ]

            if isinstance(v, classmethod):
                @wraps(v, assigned=items)
                def wrapped(cls: AbstractBase, *args: Any, _func = v.__func__, **kws: Any) -> Any:
                    if hasattr(cls, "_lock"):
                        with cls._lock:
                            return _func(cls, *args, **kws)
                    return _func(cls, *args, **kws)
            else:
                @wraps(v, assigned=items)
                def wrapped(self: AbstractBase, *args: Any, _func: Callable[..., Any]=v, **kws: Any) -> Any:
                    if hasattr(self, "_lock"):
                        with self._lock:
                            return _func(self, *args, **kws)
                    return _func(self, *args, **kws)

            if isinstance(v, classmethod):
                wrapped.__signature__ = signature(v.__func__)
            else:
                wrapped.__signature__ = signature(v)  # type: ignore[has-type]

            if isinstance(v, classmethod):
                # noinspection PyTypeChecker
                setattr(cls, k, classmethod(wrapped))
            else:
                setattr(cls, k, wrapped)  # type: ignore[has-type]

    @classmethod
    def __handle_autoinit__(cls, **kwargs) -> None:
        """
        (Internal method) Injects auto-initing.
        """

        # TODO: create dictionary-based mapping for different classes based on their __qualname__
        # TODO: for allowing multiple inheritance. Do not use __name__ since it can differ based on
        # TODO: the scope.

        if cls.__dict__.get("__children_autoinit__", False):
            def __init_subclass__(cls2, _func=cls.__init_subclass__.__func__, **kw: Any) -> None:  # type: ignore[no-untyped-def,attr-defined]
                if cls2.__dict__.get("__autocall_init__", True):
                    cls2.__autocall_init__ = True

                cls2.__calling_super__ = cls

                _func(cls2, **kw)  # type: ignore[unused-ignore]

                super().__init_subclass__(**kwargs)

            def __init__(self, *args, _func=cls.__init__, **kws):  # type: ignore[no-untyped-def]
                #if self.__class__.__name__ in "ABCDE": print(self)
                self.__autoinit_flag_init_called__ = True
                _func(self, *args, **kws) # type: ignore[unused-ignore]

            cls.__init_subclass__ = classmethod(__init_subclass__)  # type: ignore[assignment,arg-type]
            cls.__init__ = __init__  # type: ignore[method-assign]

        if cls.__dict__.get("__autocall_init__", False):

            def __init__(self, *args, _func = cls.__dict__.get("__init__", lambda *args, **kws: ...), **kws):  # type: ignore[no-untyped-def]

                _func(self, *args, **kws)  # type: ignore[unused-ignore]

                if getattr(self, "__autocall_init__", False):

                    i = self.__calling_super__
                    if not getattr(i, "__autoinit_flag_init_called__", False):

                        try:
                            i.__init__(self, *args, **kwargs)
                        except TypeError as _:
                            if len(signature(i.__init__).parameters) == 1:
                                i.__init__(self)

            __init__._wrapped_ = cls.__init__

            cls.__init__ = __init__  # type: ignore[method-assign]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Used to auto-lock user-defined classes.
        Every class that's not in Autumn or is inherited from a class outside autumn
        is considered user-defined.

        Flags:
            __no_new__: Cannot call the __new__ of this class.
            __children_autoinit__: Automatically calls the init of all children.
            __autocall_init__: Removes the effect of parent __children_autoinit__
        """

        cls.__handle_no_new__()

        cls.__handle_autoinit__(**kwargs)

        if not "__signature__" in cls.__dict__:
            if "__init__" in cls.__dict__:
                cls.__signature__ = signature(cls.__init__)  # type: ignore[attr-defined]

        cls.__handle_locking__()

        super().__init_subclass__(**kwargs)

    @abc.abstractmethod
    def build(self, **kwargs: Any) -> str:
        """
        Builds the class(e.g., style, tag, etc...).

        :param kwargs: The options to use.
        :return: The build's output.
        """

    def before_build(self, **kwargs: Any) -> str | None:
        """
        The function called before the building of the tag(s).

        :returns: The final item OR nothing(so the normal process continues).
        """

    def __deepcopy__(self, memo: Any) -> Any:
        """
        A safe copy that recreates the lock instead of deep copying it.

        :return: Deepcopy of this object.
        """
        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new

        for k, v in self.__dict__.items():
            if k == '_lock':
                setattr(new, k, threading.Lock())
                continue

            try:
                setattr(new, k, copy.deepcopy(v, memo))
            except TypeError as e:
                raise TypeError(f"Object {self.__class__.__name__}.{k} raised deepcopy error") from e
        return new

    def copy(self, item: str) -> Any:
        """
        Copies an item from this object. The item MUST have a copy attribute.

        :param item: The item's name.
        :return: the copy.
        """

        if hasattr(self, "_lock"):
            lock = self._lock
        else:
            lock = threading.Lock()

        with lock:
            if isinstance(getattr(type(self), item), property):
                if hasattr(self, "_" + item):
                    out = getattr(self, "_" + item)

                    if hasattr(out, "copy"):
                        return out.copy()
                    else:
                        return out
            else:
                return getattr(self, item)

        out = getattr(self, item)

        with lock:
            if hasattr(out, "copy"):
                return out.copy()
            return out