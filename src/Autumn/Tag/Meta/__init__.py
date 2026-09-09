from .cdn import Cdn
from .link import Link
from .script import Script
from .head import Head
from .meta import Meta as MetaTag
from .title import Title
from .script_unavailable import ScriptUnavailable

class Meta:
    """
    Meta - The package containing all the meta tags that are going to be used
    for SEO/Browser purposes. They often don't have visual effects, and have no visual effects in the Page's content.

    The one notable exception that DOES have a visual effect is Title,
    that changes the title of the HTML document(The autumn page manager handles title and charset alongside viewport).
    """

    Cdn = Cdn
    Link = Link
    Script = Script
    Head = Head
    Meta = MetaTag
    Title = Title
    ScriptUnavailable = ScriptUnavailable