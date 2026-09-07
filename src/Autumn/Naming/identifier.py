import dataclasses
import threading

from markupsafe import escape


@dataclasses.dataclass
class Identifier:
    """
    The class used to hold CSS/HTML identifiers.
    """
    name: str

    _lock = threading.Lock()

    def __post_init__(self):
        self.name = escape(self.name)

    def __str__(self):
        with self._lock:
            return self.name.replace(" ", "-").replace("\n", "-").replace("\t", "-")