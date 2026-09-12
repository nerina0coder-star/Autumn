import threading
import unittest
from typing import Any

from Autumn import AbstractBase  # type: ignore[import-not-found]
from Autumn.decorators import no_lock, allow_lock, disable_autoinit, only_self, \
    use_as_hook  # type: ignore[import-not-found]


class Test(unittest.TestCase):

    def test_classmethod_wrap_works(self) -> None:

        classmeth_called = []

        class Class(AbstractBase):

            def build(self, **kwargs: Any) -> str: return ""

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

            def __init_hook__(self) -> None:
                flags["base_called"].append(True)

        @use_as_hook()
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

    def test_base_autoinit_ignores_class_when_has_autocall_init(self) -> None:

        flags = {
            "A-Called": False,
            "B-Called": False
        }

        class A(AbstractBase):

            __children_autoinit__ = True

            def __init_hook__(self) -> None:
                flags["A-Called"] = True

            def build(self, **kwargs: Any) -> str:
                return ""


        class B(A):

            @disable_autoinit
            def __init__(self):
                flags["B-Called"] = True

        B()

        self.assertFalse(flags["A-Called"])
        self.assertTrue(flags["B-Called"])

    def test_autoinit_works_with_multiple_children_autoinit_exists(self):

        flags = {
            "A-Called": [],
            "B-Called": [],
            "C-Called": [],
            "D-Called": []
        }

        @use_as_hook()
        class A(AbstractBase):
            __children_autoinit__ = True

            def build(self, **kwargs: Any) -> str:
                return ""

            def __init__(self) -> None:
                flags["A-Called"].append(True)

        @use_as_hook()
        class B(A):

            def __init__(self) -> None:
                flags["B-Called"].append(True)

        @use_as_hook()
        class C(B):
            __children_autoinit__ = True

            def __init__(self) -> None:
                flags["C-Called"].append(True)

        class D(C):

            def __init__(self) -> None:
                flags["D-Called"].append(True)

        def clear() -> None:
            for v in flags.values():
                v.clear()

        D()

        self.assertEqual(flags["A-Called"], [True])
        self.assertEqual(flags["B-Called"], [])
        self.assertEqual(flags["C-Called"], [True])
        self.assertEqual(flags["D-Called"], [True])

        clear()

        D()
        C()

        self.assertEqual(flags["A-Called"], [True, True])
        self.assertEqual(flags["B-Called"], [])
        self.assertEqual(flags["C-Called"], [True, True])
        self.assertEqual(flags["D-Called"], [True])

        clear()

        D()
        C()
        B()

        self.assertEqual(flags["A-Called"], [True, True, True])
        self.assertEqual(flags["B-Called"], [True])
        self.assertEqual(flags["C-Called"], [True, True])
        self.assertEqual(flags["D-Called"], [True])

        clear()

        D()
        C()
        B()
        A()

        self.assertEqual(flags["A-Called"], [True, True, True, True])
        self.assertEqual(flags["B-Called"], [True])
        self.assertEqual(flags["C-Called"], [True, True])
        self.assertEqual(flags["D-Called"], [True])

    def test_params_to_parent_works_when_doing_autoinit(self):

        class A(AbstractBase):
            __children_autoinit__ = True

            def build(self, **kwargs: Any) -> str:
                return ""

            def __init_hook__(self, *, a):
                assert a == "test"

        self2 = self
        called = []

        class B(A):
            def __init__(self, b):
                self.b = b

            def __params_to_parent__(self, parent, *args, **kwargs):
                called.append(True)
                self2.assertIs(parent, A)
                self2.assertEqual(kwargs, {})
                self2.assertEqual(args, (self.b,))

                return tuple(), {"a": self.b}

        B("test")
        self.assertEqual(called, [True])

    def test_calling_super_replacement_changes_the_init_order(self):

        order = []

        class A(AbstractBase):
            __children_autoinit__ = True

            def __init_hook__(self):
                order.append(A)

            def build(self, **kwargs: Any) -> str:
                return ""

        class B(A):
            __children_autoinit__ = True

            def __init_hook__(self):
                order.append(B)

        changed_order = [False]

        class C(B):

            def __init__(self):
                if changed_order[0]:
                    self.__calling_super__ = [B, A]
                else:
                    self.__calling_super__ = [A, B]
                changed_order[0] = not changed_order[0]

        C()

        self.assertEqual(order, [A, B])

        order.clear()

        C()

        self.assertEqual(order, [B, A])

    def test_only_self_works(self):

        called = []

        @only_self
        class A(AbstractBase):  # type: ignore[misc]

            __children_autoinit__ = True

            def build(self, **kwargs: Any) -> str: return ""

            def __init_hook__(self) -> None:
                called.append(True)
                assert self.b == "test"

        class B(A):

            def __init__(self, b):
                self.b = b

        B("test")
        self.assertTrue(hasattr(B, "__params_to_parent__"))
        self.assertTrue(hasattr(B.__init__, "_wrapped_"))
        self.assertEqual(called, [True])

    def test_no_new_prevents_calling_new(self):

        class A(AbstractBase):
            __no_new__ = True

            def build(self, **kwargs: Any) -> str: return ""

        with self.assertRaises(RuntimeError,
                               msg="Cannot create class A, class declared "
                               "No New."):
            A()
