import enum


class AsAttribute(enum.Enum):
    """
    A class that represents what you can put in an as attribute of a link.
    """

    AUDIO = "audio"
    """Audio file."""

    DOCUMENT = "document"
    """An HTML document intended to be embedded in a <frame> or <iframe>."""

    TO_BE_IN_EMBEDDED = "embed"
    "Resource to be embedded inside an Embed element."

    TO_BE_FETCHED = "fetch"
    """Resource accessed by a fetch or XHR request (e.g., JSON, WebAssembly)."""

    FONT = "font"
    """Font file."""

    IMAGE = "image"
    """Image file."""

    TO_BE_IN_OBJECT = "object"
    """Resource to be embedded inside an Object element."""

    SCRIPT = "script"
    """JavaScript file."""

    STYLESHEET = "style"
    """CSS stylesheet."""

    WEB_VTT = "track"
    """WebVTT file."""

    VIDEO = "video"
    """Video file."""

    WEB_WORKER = "worker"
    """Web Worker or SharedWorker."""

    SHARED_WORKER = "worker"
    """Web Worker or SharedWorker."""