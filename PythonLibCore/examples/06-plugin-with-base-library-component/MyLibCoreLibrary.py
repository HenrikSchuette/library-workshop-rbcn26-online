from robotlibcore import keyword, DynamicCore, PluginParser
from robot.api import logger


class LibraryComponent:
    def __init__(self, library=None):
        self.library = library


class MyLibCoreLibrary(DynamicCore):
    def __init__(self, plugins):
        # here we pass the library instance to the plugin components
        library_components = PluginParser(LibraryComponent, [self]).parse_plugins(
            plugins
        )
        super().__init__(library_components)

    @keyword
    def mykeyword(self):
        logger.info("Executing mykeyword...")

    @keyword
    def my_failing_keyword(self):
        raise Exception("This keyword always fails.")

    @keyword
    def take_screenshot(self):
        logger.info("Taking a screenshot...")
