import threading
import unittest
from typing import Any

from Autumn import AbstractBase
from Autumn.decorators import no_lock, allow_lock, disable_autoinit


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

    def test_base_autoinits_children_when_class_has_children_autoinit(self):

        flags = {
            "base_called": [],
            "called_child": [],
            "called_grandchildren": []
        }

        class A(AbstractBase):
            __children_autoinit__ = True

            def build(self, **kwargs: Any) -> str:
                return ""

            def __init__(self) -> None:
                flags["base_called"].append(True)

        class B(A):

            def __init__(self) -> None:
                flags["called_child"].append(True)

        class C(B):

            def __init__(self) -> None:
                flags["called_grandchildren"].append(True)

        B()
        C()
        C()

        self.assertEqual(flags["base_called"], [True, True, True])
        self.assertEqual(flags["called_child"], [True])
        self.assertEqual(flags["called_grandchildren"], [True, True])

    def test_base_autoinit_ignores_class_when_has_autocall_init(self):

        flags = {
            "A-Called": False,
            "B-Called": False
        }

        class A(AbstractBase):

            __children_autoinit__ = True

            def __init__(self):
                flags["A-Called"] = True

            def build(self, **kwargs: Any) -> str:
                return ""

        @disable_autoinit
        class B(A):

            def __init__(self):
                flags["B-Called"] = True

        B()

        self.assertFalse(flags["A-Called"])
        self.assertTrue(flags["B-Called"])

"""    def test_autoinit_works_with_multiple_children_autoinit_exists(self):

        flags = {
            "A-Called": [],
            "B-Called": [],
            "C-Called": [],
            "D-Called": []
        }

        class A(AbstractBase):
            __children_autoinit__ = True

            def build(self, **kwargs: Any) -> str:
                return ""

            def __init__(self) -> None:
                flags["A-Called"].append(True)

        class B(A):

            def __init__(self) -> None:
                flags["B-Called"].append(True)

        class C(B):
            __children_autoinit__ = True

            def __init__(self) -> None:
                flags["C-Called"].append(True)

        class D(C):

            def __init__(self) -> None:\
                flags["D-Called"].append(True)

        def clear():
            for v in flags.values():
                v.clear()

        D()

        self.assertEqual(flags["A-Called"], [True])
        self.assertEqual(flags["B-Called"], [])
        self.assertEqual(flags["C-Called"], [True])
        self.assertEqual(flags["D-Called"], [True])
        """