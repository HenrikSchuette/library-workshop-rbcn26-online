from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from LibInstance import LibInstance
from robotlibcore import keyword


class BaseLibraryComponent:
    def __init__(self, library: LibInstance | None = None):
        self.library = library


class LibraryComponent(BaseLibraryComponent):
    @keyword
    def library_component_keyword(self):
        return self.library.library_property
