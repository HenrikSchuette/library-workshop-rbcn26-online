from robotlibcore import keyword, DynamicCore
from robot.api import logger
from pathlib import Path


class MyLibCoreLibrary(DynamicCore):
    def __init__(self, translation: Path):
        super().__init__([], translation=translation.absolute())

    @keyword
    def my_keyword(self):
        logger.info("Executing my_keyword...")
