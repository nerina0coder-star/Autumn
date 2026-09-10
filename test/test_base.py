import unittest

from typing import Any

from Autumn import new, Base, current_base  # type: ignore[import-not-found]

class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.base = new()

    def test_wrapping(self) -> None:
        @self.base.ctrl
        class A:
            ...

        a = A()

        setattr(self.base.read("wrapped", "get", 0), "hello", 1)

        self.assertEqual(len(self.base.wrapped), 1)
        self.assertTrue(hasattr(self.base.wrapped[0], "hello"))
        self.assertIs(self.base.read("wrapped", "get", 0), a)

        with self.base:
            self.assertEqual(len(current_base.wrapped), 1)

        del self.base.wrapped

        self.assertEqual(len(self.base.wrapped), 0)

    def test_merging(self) -> None:
        other = new()

        @self.base.ctrl
        class A:
            ...

        @other.ctrl
        class B:
            ...

        A()
        B()

        base = Base.merge(other, self.base)

        self.assertIsNot(base, self.base)
        self.assertIs(base, other)

        self.assertEqual(len(base.wrapped), 2)

        new_base = other.merge_new(self.base)

        self.assertIsNot(new_base, self.base)
        self.assertIsNot(new_base, other)

        self.assertEqual(len(base.wrapped), 2)

        for i in new_base._wrapped:
            self.assertIs(i.__autumn_base__, new_base)

    def test_extension_registers(self) -> None:

        self_ = self

        class Extension:

            def __init__(self) -> None:
                self_.base.extensions = self

        Extension()

        self.assertEqual(len(self.base.extensions), 1)

    def test_extension_exception_hook_with_context(self) -> None:

        called = []

        self_ = self
        class Extension:
            def __init__(self) -> None:
                self_.base.extensions = self

            def _at_exception(self, **kwargs: Any) -> None:
                called.append("any")

                self_.assertIsNone(kwargs.get("instance"))
                self_.assertIs(type(kwargs.get("exception")), RuntimeError)
                self_.assertIsNone(kwargs.get("kwargs"))
                self_.assertIsNone(kwargs.get("args"))

        Extension()
        Extension()

        def test():
            with self.base:
                raise RuntimeError

        self.assertRaises(RuntimeError, test)
        self.assertTrue(called)

    def test_extension_wrapped(self) -> None:

        self_ = self
        class Extension:
            def __init__(self) -> None:
                self_.base.extensions = self

        for i in range(10):
            self.assertTrue(hasattr(Extension(), "__autumn_base__"))
            self.assertEqual(len(self.base.extensions), i + 1)
            self.assertEqual(len(self.base.wrapped), i + 1)

    def test_extension_exception_hook_with_wrapped(self) -> None:

        called_hook = []
        called_init: list[str] = []
        called_something: list[str] = []

        @self.base.ctrl()
        class Wrapped:
            def __init__(self) -> None:
                if not called_init:
                    called_init.append("smt")
                    raise Exception("smt")

            def something(self) -> None:
                if not called_something:
                    called_something.append("smt")
                    raise Exception("smt")

        self2 = self

        class Ext:
            def __init__(self) -> None:
                self2.base.extensions = self

            def _at_exception(self, **kwargs: Any) -> None:
                self2.assertIsNotNone(kwargs.get("instance"))
                self2.assertIsNotNone(kwargs.get("kwargs"))
                self2.assertIsNotNone(kwargs.get("args"))
                self2.assertIsNotNone(kwargs.get("exception"))
                called_hook.append("smt")

        ext = Ext()

        with self.assertRaises(Exception, msg="smt"):
            Wrapped()

        self.assertTrue(called_init)
        self.assertEqual(len(called_hook), 1)

        with self.assertRaises(Exception, msg="smt"):
            Wrapped().something()

        self.assertTrue(called_something)
        self.assertEqual(len(called_hook), 2)

        Wrapped().something()

    def test_ownership(self) -> None:

        base2 = new()

        self_ = self
        class Extension:

            def __init__(self) -> None:
                self_.base.extensions = self

        ext = Extension()

        one = Extension.__autumn_base__  # type: ignore[attr-defined]

        base2.own(Extension)

        two = Extension.__autumn_base__  # type: ignore[attr-defined]

        ext2 = Extension()

        self.assertIsNot(one, two)
        self.assertEqual(len(self.base.wrapped), 1)
        self.assertEqual(len(base2.wrapped), 1)

    def test_doesnt_wrap_when_decorated_with_allow_unsafe(self) -> None:
        base = self.base

        flags = {
            "wrapped": False,
        }

        @base.ctrl()
        class Wrapped:
            @base.decorators.Safety.safe(False)
            def smt(self) -> None:
                raise RuntimeError("smt smt")

        class Extension:
            def __init__(self) -> None:
                base.extensions = self

            def _at_exception(self, **kwargs):
                flags["wrapped"] = True

        Extension()

        with self.assertRaises(RuntimeError, msg="smt smt"):
            Wrapped().smt()


        self.assertFalse(flags["wrapped"])
