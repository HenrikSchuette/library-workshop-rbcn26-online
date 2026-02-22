from robotlibcore import keyword, DynamicCore
from library_components import LibraryComponent


class MyLibCoreLibrary(DynamicCore):
    def __init__(self):
        library_components = [LibraryComponent()]
        super().__init__(library_components)

    @keyword
    def my_keyword(self):
        """An awesome keyword that does something great."""
        return "my_keyword executed!"
