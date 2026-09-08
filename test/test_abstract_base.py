import threading
import unittest
from typing import Any

from Autumn import AbstractBase
from Autumn.decorators import no_lock, allow_lock


class Test(unittest.TestCase):

    def test_classmethod_wrap_works(self) -> None:

        classmeth_called = []

        class Class(AbstractBase):

            @classmethod
            def meth(cls: Any) -> None:
                classmeth_called.append(True)

            __before__ = [meth]

        Class.meth()

        self.assertIsNot(Class.meth, Class.__before__[0])

        checking = [
            "__annotations__",
            "__doc__",
            "__name__",
            "__module__",
            "__qualname__",
        ]

        for i in checking:
            true = getattr(Class.__before__[0], i)
            mock = getattr(Class.meth, i)

            if callable(mock):
                self.assertEqual(true(), mock())
            else:
                self.assertEqual(true, mock)

        self.assertTrue(classmeth_called)

    def test_method_ignored_when_decorated_with_no_lock(self) -> None:
        locked = []
        class Class(AbstractBase):

            def __init__(self) -> None:
                self._lock = threading.Lock()


            def build(self, **kwargs: Any) -> str:
                return ""

            @no_lock
            def meth(self) -> "Class":
                locked.append(self._lock.locked())
                return self

        cls = Class()
        cls.meth()

        self.assertFalse(locked[0])

    def test_method_locked_when_decorator_allow_lock_nullifies_no_lock(self) -> None:

        locked = []
        class Class(AbstractBase):

            def __init__(self) -> None:
                self._lock = threading.Lock()

            def build(self, **kwargs: Any) -> str:
                return ""

            @allow_lock
            @no_lock
            def meth(self) -> "Class":
                locked.append(self._lock.locked())
                return self

        cls = Class()
        cls.meth()

        self.assertTrue(locked[0])
