import unittest

from Autumn import new
from Autumn.Tag.Enums.Meta import ScriptType, LinkType
from Autumn.Tag.Enums import MimeType
from run_tests import write


class Test(unittest.TestCase):
    def setUp(self):
        base = new()
        self.base = base
        self.tag = base.tag
        self.page = base.page

        self.auto = '''<meta name="viewport" content="width=device-width,initial-scale=1.0"><meta charset="UTF-8">'''

    def test_meta_custom(self):

        page = self.page.require(self.tag.meta.Cdn("script", "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4", script_type=ScriptType.JS)).new("my-page")
        children = [
            self.tag.meta.Meta(name="CSRF", content="guess-what"),
        ]
        head = self.tag.meta.Head(*children)

        self.assertMultiLineEqual(head.build(),
                         "<head>" +
                         self.auto +
                         '<meta name="CSRF" content="guess-what">'
                         "</head>")

        page.tag(head)

        write(page.build(), "meta_meta_custom.html")

    def test_link_custom(self):

        page = self.page.new("my-page")

        children = [
            self.tag.comment("This is not the correct way to add Tailwind CSS in HTML, but this is also a test."),
            self.tag.meta.Link("https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4",
                               LinkType.STYLESHEET,
                               as_=self.tag.e.Meta.AsAttribute.STYLESHEET,
                               type_=MimeType.JS),
        ]

        head = self.tag.meta.Head(*children)

        self.assertMultiLineEqual(head.build(),
                         "<head>"
                         + self.auto +
                         "<!-- This is not the correct way to add Tailwind CSS in HTML, but this is also a test. -->"
                         '<link href="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" rel="stylesheet" as="style" type="application/javascript">'
                         "</head>")

        page.tag(head)

        write(page.build(), "meta_link_custom.html")

    def test_script(self):

        page = self.page.new("my-page")

        children = [
            self.tag.meta.Script("https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4", ScriptType.JS),
            self.tag.meta.ScriptUnavailable("Your browser is too old, it does not support JS. Upgrade."),
            self.tag.comment("The above is all I added, the ones below are added by Autumn."),
        ]

        head = self.tag.meta.Head(*children)

        self.assertMultiLineEqual(head.build(),
                         "<head>"
                         + self.auto +
                         '<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4" type="application/javascript"></script>'
                         "<noscript>Your browser is too old, it does not support JS. Upgrade.</noscript>"
                         "<!-- The above is all I added, the ones below are added by Autumn. -->"
                         "</head>")