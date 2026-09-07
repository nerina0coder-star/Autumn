import enum

from Autumn.Tag.Enums import MimeType


class ScriptType(enum.Enum):
    """
    Different types of scripts.
    All script types are Module(ES6), JS(Default), JSON(For holding Data).
    """

    MODULE = "module"
    JS = str(MimeType.JS.value)
    JSON = str(MimeType.JSON.value)

    def __str__(self) -> str:
        return self.value
