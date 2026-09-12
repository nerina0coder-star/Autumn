import unittest

from Autumn import new


class Test(unittest.TestCase):

    def setUp(self):
        base = new()
        self.tag = base.tag

        class Div(self.tag.Tag):
            def __init__(self, *content, classes = None, identifier = None):

                self.name = "div"
                self.closable = True
                self.tag = [*content]
                self.classes = classes or []
                self.identifier = identifier

                super().__init__()

        self.div = Div

    def test_identifier_finder(self):

        div1 = self.div(identifier="one")
        div2 = self.div(identifier="two")
        div3 = self.div(identifier="three")
        div4 = self.div(identifier="four")
        div5 = self.div(identifier="five")
        div6 = self.div(identifier="six")
        div7 = self.div(identifier="seven")
        div7duplicate = self.div(identifier="seven")

        "" >> div1 >> div2 >> div3 >> div4 >> div5 >> div6 >> div7 >> div7duplicate

        self.assertEqual(div7duplicate.identifiers(), list(reversed(["one", "two", "three", "four", "five", "six", "seven", "seven"])))
        self.assertEqual(div7duplicate.duplicate_identifiers(), ["seven"])
