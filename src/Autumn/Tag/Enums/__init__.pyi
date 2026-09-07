from typing import ClassVar
from .mime_type import MimeType as MimeType
from .language import Language as Language
from .Meta import Meta

class Enums:

    MimeType: ClassVar[type[MimeType]]
    Language: ClassVar[type[Language]]
    Meta: ClassVar[type[Meta]]
