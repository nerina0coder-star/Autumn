import unittest

from Autumn import new  # type: ignore[import-not-found]


class Test(unittest.TestCase):

    def setUp(self) -> None:
        base = new()
        self.tag = base.tag
        self.page = base.page
        self.style = base.style

        self.prefix = "styling_colors_"
        # TODO