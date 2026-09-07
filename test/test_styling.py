import unittest

from Autumn import new


class Test(unittest.TestCase):

    def setUp(self):
        base = new()
        self.tag = base.tag
        self.page = base.page
        self.style = base.style

        self.prefix = "styling_colors_"
        # TODO