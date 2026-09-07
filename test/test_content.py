import unittest

from Autumn import new
from run_tests import write


class Test(unittest.TestCase):

    def setUp(self):
        base = new()
        self.tag = base.tag
        self.page = base.page
        self.Base = base

        self.prefix = "content_"

    # Custom

    def test_div(self):

        page = self.page.new("my-page")

        class Div(self.tag.Tag):

            def __init__(self):
                self.true = None
                self.name = "div"
                self.closable = True
                super().__init__()

            def do_print(self):
                self.true = True

        self.assertEqual(Div().build(),
                         "<div></div>")

        page.tag(Div())
        page.tags[0].do_print() # type: ignore
        self.assertTrue(page.tags[0].true) # type: ignore
        write(page.build(), self.prefix + "custom_div.html")