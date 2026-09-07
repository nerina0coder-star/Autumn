import enum
from pathlib import Path


class MimeType(enum.Enum):
    """
    A class holding many mime types used in real world cases.
    Note that for extensions that start with a number, put a trailing _ to find them.
    """
    HTML = "Text/html"
    HTM = HTML
    SHTML = HTML
    CSS = "Text/css"
    XML = "Text/xml"
    GIF = "image/gif"
    JPEG = "image/jpeg"
    JPG = JPEG
    JS = "application/javascript"
    ATOM = "application/atom+xml"
    RSS = "application/rss+xml"

    MML = "Text/mathml"
    TEXT = "Text/plain"
    JAD = "Text/vnd.sun.j2me.app-descriptor"
    WML = "Text/vnd.wap.wml"
    HTC = "Text/x-component"

    AVIF = "image/avif"
    PNG = "image/png"
    SVG = "image/svg+xml"
    SVGZ = SVG
    TIFF = "image/tiff"
    TIF = TIFF
    WBMP = "image/vnd.wap.wbmp"
    WEBP = "image/webp"
    ICO = "image/x-icon"
    JNG = "image/x-jng"
    BMP = "image/x-ms-bmp"

    WOFF = "font/woff"
    WOFF2 = "font/woff2"

    JAR = "application/java-archive"
    WAR = JAR
    EAR = JAR
    JSON = "application/json"
    HQX = "application/mac-binhex40"
    DOC = "application/msword"
    PDF = "application/pdf"
    PS = "application/postscript"
    EPS = PS
    AI = PS
    RTF = "application/rtf"
    M3U8 = "application/vnd.apple.mpegurl"
    KML = "application/vnd.google-earth.kml+xml"
    KMZ = "application/vnd.google-earth.kmz"
    XLS = "application/vnd.ms-excel"
    EOT = "application/vnd.ms-fontobject"
    PPT = "application/vnd.ms-powerpoint"
    ODG = "application/vnd.oasis.opendocument.graphics"
    ODP = "application/vnd.oasis.opendocument.presentation"
    ODS = "application/vnd.oasis.opendocument.spreadsheet"
    ODT = "application/vnd.oasis.opendocument.Text"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    WMLC = "application/vnd.wap.wmlc"
    WASM = "application/wasm"
    _7Z = "application/x-7z-compressed"
    CCO = "application/x-cocoa"
    JARDIFF = "application/x-java-archive-diff"
    JNLP = "application/x-java-jnlp-file"
    RUN = "application/x-makeself"
    PL = "application/x-perl"
    PM = PL
    PRC = "application/x-pilot"
    PDB = PRC
    RAR = "application/x-rar-compressed"
    RPM = "application/x-redhat-package-manager"
    SEA = "application/x-sea"
    SWF = "application/x-shockwave-flash"
    SIT = "application/x-stuffit"
    TCL = "application/x-tcl"
    TK = TCL
    DER = "application/x-x509-ca-cert"
    PEM = DER
    CRT = DER
    XPI = "application/x-xpinstall"
    XHTML = "application/xhtml+xml"
    XSPF = "application/xspf+xml"
    ZIP = "application/zip"

    BIN = "application/octet-stream"
    EXE = BIN
    DLL = BIN
    DEB = "application/octet-stream"
    DMG = "application/octet-stream"
    ISO = "application/octet-stream"
    IMG = ISO
    MSI = "application/octet-stream"
    MSP = MSI
    MSM = MSI

    MID = "audio/midi"
    MIDI = MID
    KAR = MID
    MP3 = "audio/mpeg"
    OGG = "audio/ogg"
    M4A = "audio/x-m4a"
    RA = "audio/x-realaudio"

    _3GPP = "video/3gpp"
    _3GP = _3GPP
    TS = "video/mp2t"
    MP4 = "video/mp4"
    MPEG ="video/mpeg"
    MPG = MPEG
    OGV = "video/ogg"
    MOV = "video/quicktime"
    WEBM = "video/webm"
    FLV = "video/x-flv"
    M4V = "video/x-m4v"
    MKV = "video/x-matroska"
    MNG = "video/x-mng"
    ASX = "video/x-ms-asf"
    ASF = ASX
    WMV = "video/x-ms-wmv"
    AVI = "video/x-msvideo"

    @staticmethod
    def guess(url: str) -> "MimeType | None":
        """
        Guesses the filetype of a file based on its extension.
        :param url:
        :return:
        """
        if "." in url[max(url.rfind("/"), url.rfind("\\")) + 1:]:
            extension = Path(url).suffix
            if extension[0].isdigit():
                extension = "_" + extension
            if extension.upper() in MimeType:
                return MimeType(extension.upper())

        return None

    def __str__(self) -> str:
        return self.value
