from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TodoLibrary import TodoLibrary


class BaseLibraryComponent:
    def __init__(self, library: TodoLibrary | None = None):
        self.library = library
