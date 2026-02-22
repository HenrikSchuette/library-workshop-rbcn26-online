from robotlibcore import keyword
from robot.api import logger


class Plugin:
    @keyword
    def plugin_keyword(self):
        logger.info("Executing plugin_keyword...")
