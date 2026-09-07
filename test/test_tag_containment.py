import unittest

from Autumn import new
from run_tests import write


class Test(unittest.TestCase):
    def setUp(self):
        base = new()
        self.page = base.page
        self.tag = base.tag

        class Span(self.tag.Tag):
            def __init__(self, *content):
                self.name = "span"
                self.closable = True
                if len(content) == 1 and isinstance(content[0], list):
                    self.tags = list(content[0])
                else:
                    self.tags = list(content)

                super().__init__()

        class Body(self.tag.Tag):
            def __init__(self, *content):
                self.name = "body"
                self.closable = True
                self.tags = list(content)

                super().__init__()

        self.tag.alias("span", Span)
        self.tag.alias("body", Body)

        self.prefix = "containment_"

    def test_lshift(self):
        

        page = self.page.new("my-page")

        body = self.tag.body() << \
               self.tag.span("Hello ") << \
               self.tag.span("World!")
        """
        The operation above is same the as:
        
        body = Body() << span("Hello ")
        
        body = body << span("World!")
        
        and also the same as:
        
        body = Body(span("Hello "), span("World!"))
        """

        self.assertMultiLineEqual(
           body.build(),
            "<body>"
            "<span>Hello </span>"
            "<span>World!</span>"
            "</body>"
        )

        page.tag(body)

        write(page.build(), self.prefix + "lshift.html")

    def test_rshift(self):

        page = self.page.new("my-page")

        body = self.tag.span("World!") >> \
               (self.tag.span("Hello ") >> self.tag.body())

        self.assertMultiLineEqual(body.build(),
                         "<body>"
                         "<span>Hello </span>"
                         "<span>World!</span>"
                         "</body>")

        page.tag(body)

        write(page.build(), self.prefix + "rshift.html")

    def test_in(self):
        page = self.page.new("my-page")

        span = self.tag.span("Hello")
        body = self.tag.body(span, self.tag.span("World!"))

        self.assertIn(span, body)
        self.assertIn(self.tag.span, body)

        page.tag(body)

        write(page.build(), self.prefix + "in")
