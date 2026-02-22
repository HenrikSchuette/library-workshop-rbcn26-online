from robotlibcore import keyword, DynamicCore
from lib_instance_components import LibraryComponent


class LibInstance(DynamicCore):
    def __init__(self):
        library_components = [LibraryComponent(self)]
        super().__init__(library_components)
        self.library_property = "Some property"

    @keyword
    def my_keyword(self):
        """An awesome keyword that does something great."""
        return "my_keyword executed!"
