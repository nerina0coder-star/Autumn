import enum


class LinkType(enum.Enum):
    """
    Different types of a link, for example, when including a CSS stylesheet, use STYLESHEET.
    Each one of them has a document to make everything clear.
    """

    STYLESHEET = "stylesheet"
    """
    Used for CSS linking.
    """

    ICON = "icon"
    """
    Used for setting a Favicon for the page.
    """

    CANONICAL = "canonical"
    """
    Specifies the preferred URL for the current document to prevent duplicate content issues.
    """

    ALTERNATE = "alternate"
    """
    Link to an alternate representation of the document, such as a translated version, a print page, or an RSS/Atom feed.
    """

    AUTHOR = "author"
    """
    Link to a page about the author of the document or article.
    """

    LICENSE = "license"
    """
    Link to the license of the document.
    """

    BOOKMARK = "bookmark"
    """
    Provides a permanent link (permalink) for the nearest ancestor section.
    """

    MANIFEST = "manifest"
    """
    Link to a manifest file(e.g., manifest.json, app.webmanifest).
    """

    SEARCH = "search"
    """
    Link to a resource that can be used to search the current document and its related pages.
    """

    PRIVACY_POLICY = "privacy-policy"
    """
    Link to the document's privacy policy.
    """

    TERMS_OF_SERVICE = "terms-of-service"
    """
    Link to the document's terms of service.
    """

    NEXT = "next"
    """
    Link to the next page after this document(used in series).
    """

    PREV = "prev"
    """
    Link to the previous page from this document(used in series).
    """

    PRELOAD = "preload"
    """
    Used to fetch an asset early with the highest priority possible.
    """

    PREFETCH = "prefetch"
    """
    Used to fetch an asset for the next page the user is likely to visit, lowest priority.
    """

    PRECONNECT = "preconnect"
    """
    Suggests the browser to preemptively connect to a third-party origin (e.g., for DNS, TCP, TLS).
    """

    DNS_PREFETCH = "dns-prefetch"
    """
    Suggests the browser to perform DNS resolution for a domain in advance.
    """

    PRERENDER = "prerender"
    """
    Suggests the browser load and render a page in the background for near-instant navigation.
    """

    MODULE_PRELOAD = "modulepreload"
    """
    Preemptively fetches a JavaScript module and its dependencies.
    """

    COMPREHENSION_DICT = "comprehension-dictionary"
    """
    Link to a compression dictionary that can be used to compress future downloads.
    """

    NO_FOLLOW = "nofollow"
    """
    Tells search engines not to follow the link or pass on "link juice".
    """

    NO_OPEN = "noopen"
    """
    Prevents the new page from accessing the window.opener object, improving security.
    """

    NO_REFERRER = "noreferer"
    """
    Prevents the Referer header from being sent when navigating.
    """

    EXTERNAL = "external"
    """
    Indicates this link is not part of the same site.
    """

    def __str__(self) -> str:
        return self.value