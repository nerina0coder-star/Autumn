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

        class Div(self.tag.Tag):
            def __init__(self, *content):
                self.name = "div"
                self.closable = True
                self.tags = list(content)

                super().__init__()

        class Br(self.tag.Tag):
            def __init__(self):
                self.name = "br"

                super().__init__()

        class Body(self.tag.Tag):
            def __init__(self, *content):
                self.name = "body"
                self.closable = True
                self.tags = list(content)

                super().__init__()

        self.tag.alias("body", Body)

        self.tag.alias("p", P)
        self.tag.alias("div", Div)
        self.tag.alias("br", Br)

        self.prefix = "arithmetic_"

    def test_multiplication(self):


        page = self.page.new("my-page")

        p1 = self.tag.p("This is a paragraph") * 2
        brs = self.tag.br() * 2
        p2 = self.tag.p("This is another paragraph") * 2

        body = self.tag.body(*[*p1, *brs, *p2])

        self.assertMultiLineEqual(body.build(),
             "<body>" +
                ("<p>This is a paragraph</p>" * 2) +
                ("<br>" * 2) +
                ("<p>This is another paragraph</p>" * 2) +
             "</body>"
        )

        page.tag(body)

        write(page.build(), self.prefix + "multiplication.html")

    def test_addition(self):


        page = self.page.new("my-page")

        content = self.tag.p("This is a paragraph") + self.tag.br() + self.tag.p("And another paragraph.")

        body = self.tag.body(*content)

        self.assertMultiLineEqual(body.build(),
             "<body>"
                 "<p>This is a paragraph</p>"
                 "<br>" 
                 "<p>And another paragraph.</p>"
             "</body>"
        )

        page.tag(body)

        write(page.build(), self.prefix + "addition.html")

    def test_subtraction(self):
        
        page = self.page.new("my-page")

        content = self.tag.div(self.tag.p("Hello!"), self.tag.p("World!"))

        # The statement below is supposed to remove World! paragraph

        var = content - self.tag.p

        self.assertEqual(var, [])
        self.assertEqual(len(content.tags), 1)
        self.assertEqual(content.tags[0].build(), "<p>Hello!</p>")

        # The statement below is supposed to return [P]

        var = content - [self.tag.p, self.tag.p]

        self.assertEqual(var, [self.tag.p])
        self.assertEqual(len(content.tags), 0)

        page.tag(content)

        write(page.build(), self.prefix + "subtraction.html")
