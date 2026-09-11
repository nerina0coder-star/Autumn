import copy
import threading
from contextvars import ContextVar
from inspect import isroutine
from warnings import warn

from werkzeug.local import LocalProxy

from Autumn.Page.page_manager import PageManager
from Autumn.Style import StyleManager
from Autumn.Tag import TagManager
from Autumn.exceptions import ContextError
from .abstract_base import AbstractBase
from .decorators import Decorators
from .Naming import Naming


class Dummy:
    def __getattr__(self, _):
        raise ContextError()


dummy = Dummy()

_base = ContextVar("base", default=None)


def _set_base(base):
    _base.set(base)


def _remove_base():
    _base.set(None)


def _current_base():
    instance = _base.get()
    if instance is None:
        return dummy
    return instance


current_base = LocalProxy(_current_base)  # type: ignore
"""
The base currently used.
"""


class Base:
    """
    Manages the interactions with Autumn.
    """

    def __init__(self):
        """
        Initializes a new Base instance.
        """
        self._pages = []

        self.page = PageManager([])
        self.tag = TagManager()
        self.style = StyleManager()
        self.name = Naming
        self.any = AbstractBase
        """
        any - the base class for all/most autumn classes.
        """

        self.decorators = Decorators

        self._extensions = []
        self._wrapped = []
        self._lock = threading.Lock()

    @property
    def extensions(self):
        """
        Returns the instances of the classes that classified themselves as extensions.

        :return: A deepcopy of the extensions.
        """
        with self._lock:
            return copy.deepcopy(self._extensions)

    @extensions.setter
    def extensions(self, value):
        """
        Classifies the given class as Extension.

        :param value: The extension to classify.
        """
        with self._lock:
            self._extensions.append(value)

        if not getattr(type(value), "_wrapped_with_autumn_base_ctrl", False):
            self.ctrl(type(value))
            self.wrapped = value
            value.__autumn_base__ = self


    @extensions.deleter
    def extensions(self):
        """
        Empties the current extension list.
        """
        with self._lock:
            self._extensions.clear()

    @property
    def wrapped(self):
        """
        Returns all the wrapped classes, including but not limited to extensions.

        :return: A deepcopy of the wrapped instances.
        """
        with self._lock:
            return copy.deepcopy(self._wrapped)

    @wrapped.setter
    def wrapped(self, value):
        """
        Adds the wrapped value to the wrapped list. (Value must be an instance)
        """

        with self._lock:
            if not getattr(type(value), "_wrapped_with_autumn_base_ctrl", False):
                raise ValueError(f"Expected a wrapped class, given {value}.")
            self._wrapped.append(value)

    @wrapped.deleter
    def wrapped(self):
        """
        Empties the current wrapped list.
        """

        with self._lock:
            self._wrapped.clear()

    def read(self, attribute, function, *args, **kwargs):
        """
        Performs a read operation on the list.

        :param attribute: The attribute to read.
        :param function: get(getitem), index, copy, count, or range(slicing).
        :param args: The arguments to give to the function.
        :param kwargs: The keyword arguments to give to the function.
        :return: The result of the read operation.
        """

        attribute = "_" + attribute

        with self._lock:
            if not function in \
                ["get", "index", "copy",
                 "count", "range"]:
                raise RuntimeError(f"Unallowed function: {function}, only get, index, copy, and range(slicing) are allowed")

            if function == "get" and len(args) == 1:
                return getattr(self, attribute)[args[0]]
            if function == "range" and len(args) == 2:
                return getattr(self, attribute)[args[0]:args[1]]
            if function == "range" and len(args) == 3:
                return getattr(self,attribute)[args[0]:args[1]:args[2]]

            return getattr(getattr(self, attribute), function)(*args, **kwargs)

    def write(self, attribute, function, *args, **kwargs):
        """
        Performs a limited write operation on the list.

        :param attribute: The attribute to write to.
        :param function: The function to call. extend, pop, or remove.
        :param args: The arguments to give to the function.
        :param kwargs: The keyword arguments to give to the function.
        :return: The result of the called function.
        """

        attribute = "_" + attribute

        with self._lock:
            if not function in \
                ["pop", "remove", "extend"]:
                raise RuntimeError(f"Unallowed function: {function}, only pop, remove, extend, and range are allowed")

            if function == "extend":
                for i in args:
                    if not getattr(type(i), "_wrapped_with_autumn_base_ctrl", False):
                        self.ctrl(type(i))
            return getattr(getattr(self, attribute), function)(*args, **kwargs)


    def ctrl(self, cls=None):
        """
        Wraps and controls the state of an unknown/not-internal class.

        :param cls: The class to wrap.
        :return: The wrapped class.
        """

        if cls is None:
            return self.ctrl

        def mock_callable(*_, **__): ...

        last_self = getattr(cls, "__init__", mock_callable)

        def init(self_, *args, **kwargs):
            if hasattr(self, "__class__"):
                base: Base = type(self_).__autumn_base__
            else:
                base: Base = self_.__autumn_base__

            with base._lock:
                for extension in base._extensions:
                    if not hasattr(extension, "_wrap") or not callable(extension._wrap):
                        continue

                    if extension is self_:
                        continue

                    extension._wrap(instance=self_, args=args, kwargs=kwargs)

                base._wrapped.append(self_)

            try:
                last_self(self_, *args, **kwargs)
            except Exception as e:
                base._notify_extensions_of_exception(instance=self_, exception=e, args=args, kwargs=kwargs)
                raise

        for i, j in cls.__dict__.items():

            if i in ["__new__", "__init__",
                     "__getattribute__", "__setattr__",
                     "__dict__", "__doc__", "__module__",
                     "__weakref__"]:
                continue

            if hasattr(j, "__allow_unsafe__") and j.__allow_unsafe__:
                continue

            if not isroutine(j):
                continue

            if isinstance(j, staticmethod):
                continue

            def out(self_, *args, _autumn_func=j, **kwargs):
                try:
                    return _autumn_func(self_, *args, **kwargs)
                except Exception as e:
                    if hasattr(self_, "__class__"):
                        base: Base = type(self_).__autumn_base__
                    else:
                        base: Base = self_.__autumn_base__
                    base._notify_extensions_of_exception(instance=self_, exception=e, args=args, kwargs=kwargs)
                    raise

            if isinstance(j, classmethod):
                setattr(cls, i, classmethod(out))
            else:
                setattr(cls, i, out)

        cls.__init__ = init

        cls._wrapped_with_autumn_base_ctrl = True
        cls.__autumn_base__ = self

        return cls

    def __enter__(self):
        """
        Enters a context to ensure if an error is raised, extensions exit gracefully.
        In this context, current_base is this instance.
        """
        _set_base(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context. If an error is raised, all extensions will be notified.
        """
        if exc_type:
            self._notify_extensions_of_exception(exception=exc_val)
        _remove_base()

    def this(self):
        """
        Returns this instance itself, useful when combined with current_base.
        """
        return self

    def merge_new(self, other):
        """
        Merges self and other, resulting in a completely new base.

        :param other: The other base.
        :return: The new base.
        """
        new = Base()

        Base.merge(new, self)
        Base.merge(new, other)

        return new

    @staticmethod
    def merge(one, two, /):
        """
        Merges the two into one.

        :param one: The one to get all the data from two.
        :param two: The one to extract data from.
        :return: param "one".
        """
        with one._lock:
            with two._lock:

                # Extensions and wrapped
                one._extensions.extend([*two._extensions])
                one._wrapped.extend([*two._wrapped])

                for i in one._wrapped:
                    if hasattr(i, "_lock"):
                        with i._lock:
                            i.__autumn_base__ = one
                    else:
                        i.__autumn_base__ = one

                # page manager
                one.page.merge(two.page)

                # tag manager
                one.tag.merge(two.tag)

                # style manager
                registering = {}
                registering.update(two.style._styles)

                one.style.register_all(**registering)

        # Done
        return one

    def own(self, cls):
        """
        Owns the given class, that's owned by another Base.
        The class must already be wrapped with Autumn.

        :param cls: The class to own.
        :raises ValueError: If the class is not wrapped already.
        """
        if not hasattr(cls, "_wrapped_with_autumn_base_ctrl"):
            raise ValueError(f"Expected a wrapped class, given {cls.__name__}")
        cls.__autumn_base__ = self

    def _notify_extensions_of_exception(self, **kwargs):
        """
        (Internal) Used to notify extensions of an acquired exception.

        :param kwargs: The kwargs to give to each extension.
        :return:
        """

        if not self._lock.acquire(True, 10):
            return
        # 10 seconds should be enough, if it passes 10 seconds, it's a deadlock.

        try:

            for extension in self._extensions:
                try:
                    if extension is kwargs.get("instance", None):
                        continue
                    if not hasattr(extension, "_at_exception") or not callable(extension._at_exception):
                        continue
                    extension._at_exception(**kwargs)
                except Exception as e:
                    warn(f"""Extension {extension.__class__.__name__}'s exception hook failed with "{e}", skipping.""")
        finally:
            if self._lock.locked():
                self._lock.release()

    def __deepcopy__(self, memo):
        """
        Custom deepcopy to prevent Lock pickling errors.
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
                raise TypeError(f"Object Base.{k} raised deepcopy error") from e
        return new