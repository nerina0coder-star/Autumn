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
        if cls.__dict__.get("__no_new__", False) and not getattr(cls.__new__, "__autumn_no_new_handled", False):

            def new(cls2: type, *__: Any, **___: Any) -> Any:
                if cls2 is cls:
                    raise RuntimeError(f"Cannot create class {cls.__name__}, class declared "
                                       "No New.")
                # noinspection PySuperArguments
                return super(cls, cls2).__new__(cls2)  # type: ignore[misc]

            setattr(new, "__autumn_no_new_handled", True)
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
                def wrapped(cls: AbstractBase, *args: Any, _func=v.__func__, **kws: Any) -> Any:
                    if hasattr(cls, "_lock"):
                        with cls._lock:
                            return _func(cls, *args, **kws)
                    return _func(cls, *args, **kws)
            else:
                @wraps(v, assigned=items)
                def wrapped(self: AbstractBase, *args: Any, _func: Callable[..., Any] = v, **kws: Any) -> Any:
                    if hasattr(self, "_lock"):
                        with self._lock:
                            return _func(self, *args, **kws)
                    return _func(self, *args, **kws)

            if isinstance(v, classmethod):
                wrapped.__signature__ = signature(v.__func__)
            else:
                wrapped.__signature__ = signature(v)  # type: ignore[has-type]

            wrapped.__no_lock__ = True  # type: ignore[has-type]

            if isinstance(v, classmethod):
                # noinspection PyTypeChecker
                setattr(cls, k, classmethod(wrapped))
            else:
                setattr(cls, k, wrapped)  # type: ignore[has-type]

    @classmethod
    def __handle_autoinit__(cls) -> None:
        """
        (Internal method) Injects auto-initing.
        """

        def get(item: str) -> Callable[..., Any]:
            out = cls.__dict__.get(item, lambda *x, **y: ...)
            if out.__dict__.get("__autumn_handled_autoinit__", False):
                return lambda *x, **y: ...
            return out  # type: ignore[no-any-return]

        def getcls(item: str) -> Callable[..., Any]:
            out = getattr(get(item), "__func__", lambda *x, **y: ...)
            if out.__dict__.get("__autumn_handled_autoinit__", False):
                return lambda *x, **y: ...
            return out

        if cls.__dict__.get("__children_autoinit__", False):
            def __init_subclass__(cls2: type[AbstractBase],
                                  _func: Callable[..., Any]=getcls("__init_subclass__"),
                                  **kw: Any) -> None:
                if cls2.__dict__.get("__autocall_init__", True):
                    setattr(cls2, "__autocall_init__", True)

                if "__calling_super__" in cls2.__dict__: cls2.__dict__["__calling_super__"].append(cls)
                else: setattr(cls2, "__calling_super__", [cls])

                _func(cls2, **kw)  # type: ignore[unused-ignore]

                if "__init__" not in cls.__dict__:
                    cls2.__init__ = lambda self, *args, **kws: ...  # type: ignore[method-assign,assignment]
                super(cls, cls2).__init_subclass__(**kw)  # type: ignore[unused-ignore]

            setattr(__init_subclass__, "__autumn_handled_autoinit__", True)
            cls.__init_subclass__ = classmethod(__init_subclass__)  # type: ignore[assignment,arg-type]

        if cls.__dict__.get("__autocall_init__", False):
            if getattr(get("__init__"), "__no_auto__", False):
                return

            def __init__(self: AbstractBase, *args: Any, _func: Callable[..., Any] = get("__init__"),
                         **kws: Any) -> Any:

                _func(self, *args, **kws)  # type: ignore[unused-ignore]

                if "__autumn_inited_list" not in self.__dict__:
                    self.__dict__["__autumn_inited_list"] = [type(self)]
                __autumn_inited_list = self.__dict__["__autumn_inited_list"]

                top = len(__autumn_inited_list) == 1

                params = lambda *a, **kw: (args, kws)

                if "__params_to_parent__" in self.__dict__:
                    params = getattr(self, "__params_to_parent__")

                calling_super = getattr(self, "__calling_super__").copy()

                for i in calling_super:

                    called: tuple[tuple[Any, ...], dict[Any, Any]] = params(i, *args, **kws)  # type: ignore[no-untyped-call]

                    arguments: tuple[Any, ...] = called[0]
                    keyword_arguments: dict[Any, Any] = called[1]

                    if i in __autumn_inited_list:
                        continue
                    __autumn_inited_list.append(i)
                    try:
                        i.__init__(self, *arguments, **keyword_arguments)
                    except TypeError as _:
                        if len(signature(i.__init__).parameters) == 1:
                            i.__init__(self)

                if top:
                    delattr(self, "__autumn_inited_list")

            __init__._wrapped_ = cls.__init__  # type: ignore[attr-defined]
            __init__.__autumn_handled_autoinit__ = True  # type: ignore[attr-defined]

            cls.__init__ = __init__  # type: ignore[assignment]

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

        if cls.__dict__.get("__already_handled__", False):
            super().__init_subclass__(**kwargs)

        cls.__handle_no_new__()

        cls.__handle_autoinit__()

        if not "__signature__" in cls.__dict__:
            if "__init__" in cls.__dict__:
                setattr(cls, "__signature__", signature(cls.__init__))

        cls.__handle_locking__()

        setattr(cls, "__already_handled__", True)

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

    def copy(self, item: str) -> Any | None:
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

                    return out.copy()

            else:
                return getattr(self, item).copy()

        return None
