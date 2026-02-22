from robotlibcore import keyword, DynamicCore
from lib_intance_components import LibraryComponent


class LibInstance(DynamicCore):
    def __init__(self):
        self.library_property = "I am a property of MyLibCoreLibrary"
        library_components = [LibraryComponent(self)]
        super().__init__(library_components)

    @keyword
    def my_keyword(self):
        """An awesome keyword that does something great."""
        return "my_keyword executed!"
