import unittest

from Autumn import new # type: ignore[import-not-found]


class Test(unittest.TestCase):

    def setUp(self) -> None:
        base = new()

        self.page = base.page
        self.style = base.style
        self.tag = base.tag
        self.name = base.name

    def test_page(self) -> None:
        page = (self.page.require(self.tag.meta.Cdn("style", "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.8/js/bootstrap.min.js"))
                .new("my-page"))

        page.tag(self.tag.meta.Head())

        self.assertMultiLineEqual(page.build(),
                                  "<!DOCTYPE html>"
                                  '<html lang="en" dir="auto">'
                                  "<head>"
                                  '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
                                  '<meta charset="UTF-8">'
                                  "<title>my-page</title>"
                                  '</head>'
                                  '</html>')

        class CustomPage(self.page.Page):  # type: ignore[misc,name-defined]
            ...

        self.page.register(CustomPage("page"))

        self.assertMultiLineEqual(page.build(),
                                  CustomPage("my-page").build())

        self.assertMultiLineEqual(page.build(),
                                  self.page.build("my-page"))

    def test_sheet(self) -> None:

        self2 = self

        class Style(self.style.Style):  # type: ignore[misc,name-defined]
            def __init__(self) -> None:
                self.styles = ["margin: 1px;", "padding: 1px;"]
                self.name = ["div", self2.name.Name("smt", "identifier", ["any"])]
                self.classes = ["margin-and-padding", self2.name.Class("cls")]
                self.identifier = ["id1", self2.name.Identifier("id2")]

                super().__init__()

        sheet = self.style.Sheet(Style())

        self.assertMultiLineEqual(sheet.build(),
                                  "div,smt#identifier.any"
                                  ",.margin-and-padding,.cls"
                                  ",#id1,#id2{margin: 1px;padding: 1px;}")
