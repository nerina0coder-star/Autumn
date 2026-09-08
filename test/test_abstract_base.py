import unittest
from typing import Any

from Autumn import AbstractBase


class Test(unittest.TestCase):

    def test_classmethod_wrap_works(self):

        classmeth_called = []

        class Class(AbstractBase):

            @classmethod
            def meth(cls: Any) -> Any | None:
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
