from robotlibcore import keyword
from robot.api import logger
from MyLibCoreLibrary import LibraryComponent


class Plugin(LibraryComponent):
    @keyword
    def plugin_keyword(self):
        self.library.mykeyword()
        logger.info("Executing plugin_keyword...")
