from robotlibcore import keyword, DynamicCore


class MyLibCoreLibrary(DynamicCore):
    def __init__(self):
        super().__init__([])

    @keyword
    def my_keyword(self):
        """An awesome keyword that does something great."""
        return "I am a property of MyLibCoreLibrary"
