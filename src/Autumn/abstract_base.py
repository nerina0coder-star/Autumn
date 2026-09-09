import abc
import copy
import threading
from collections.abc import Callable
from inspect import signature, isroutine
from typing import Any


class AbstractBase(abc.ABC):
    """
    The base of most, if not all, of classes in Autumn.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Used to auto-lock user-defined classes.
        Every class that's not in Autumn or is inherited from a class outside autumn
        is considered user-defined.
        """

        if cls.__dict__.get("__no_new__", False):

            def new(cls2: type, *__: Any, **___: Any) -> Any:
                if cls2 is cls:
                    raise RuntimeError(f"Cannot create class {cls.__name__}, class declared "
                                    "No New.")
                return super().__new__(cls2)  # type: ignore[misc]

            cls.__new__ = new  # type: ignore[method-assign,assignment]

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

            if isinstance(v, classmethod):
                def wrapped(cls: AbstractBase, *args: Any, _func = v.__func__, **kws: Any) -> Any:
                    if hasattr(cls, "_lock"):
                        with cls._lock:
                            return _func(cls, *args, **kws)
                    return _func(cls, *args, **kws)
            else:
                def wrapped(self: AbstractBase, *args: Any, _func: Callable[..., Any]=v, **kws: Any) -> Any:  # type: ignore[misc]
                    if hasattr(self, "_lock"):
                        with self._lock:
                            return _func(self, *args, **kws)
                    return _func(self, *args, **kws)

            items = [
                "__name__",
                "__doc__",
                "__str__",
                "__qualname__",
                "__module__",
                "__annotations__",
                "__type_params__"
            ]

            for i in items:
                if i in dir(v):
                    setattr(wrapped, i, getattr(v, i))

            if isinstance(v, classmethod):
                # noinspection PyTypeChecker
                setattr(cls, k, classmethod(wrapped))
            else:
                setattr(cls, k, wrapped)

        if not "__signature__" in cls.__dict__:
            if "__init__" in cls.__dict__:
                cls.__signature__ = signature(cls.__init__)  # type: ignore[attr-defined]

        try:
            super().__init_subclass__(**kwargs)
        except TypeError as e:
            if "takes 0 positional argument but" in str(e):
                super().__init_subclass__()
            raise

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