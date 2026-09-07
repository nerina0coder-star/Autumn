import unittest

from Autumn import new
from run_tests import write


class Test(unittest.TestCase):
    def setUp(self):
        base = new()
        self.tag = base.tag
        self.page = base.page

        class P(self.tag.Tag):
            def __init__(self, *content):
                self.name = "p"
                self.closable = True
                self.tags = list(content)

                super().__init__()

        self.tag.alias("p", P)

        self.prefix = "comparison_"

    def test_equality(self):
        

        page = self.page.new("my-page")

        p1 = self.tag.p("Hello!")
        p2 = self.tag.p("World!")

        self.assertEqual(p1, p2)

        if p1 == p2:
            page.tag(p1)
        else:
            page.tag(p2)

        write(page.build(), self.prefix + "equality.html")

    def test_greaterThan(self):
        

        tag = self.tag.Tag

        page = self.page.new("my-page")

        p1: tag = self.tag.p("Hello!")
        p2: tag = self.tag.p("World!")

        p1.worth = 2

        self.assertGreater(p1, p2)

        if p1 > p2:
            page.tag(p1)
        else:
            page.tag(p2)

        write(page.build(), self.prefix + "greater.html")


    def test_lessThan(self):
        

        tag = self.tag.Tag

        page = self.page.new("my-page")

        p1: tag = self.tag.p("Hello!")
        p2: tag = self.tag.p("World!")

        p2.worth = 2

        self.assertLess(p1, p2)

        if p1 > p2:
            page.tag(p1)
        else:
            page.tag(p2)

        write(page.build(), self.prefix + "less.html")
