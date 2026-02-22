from robotlibcore import keyword, DynamicCore
from robot.api import logger
from pathlib import Path


class MyLibCoreLibrary(DynamicCore):
    def __init__(self, translation: Path):
        super().__init__([], translation=translation.absolute())

    @keyword
    def my_keyword(self):
        logger.info("Executing my_keyword...")

    @keyword
    def my_failing_keyword(self):
        raise Exception("This keyword always fails.")

    @keyword
    def take_screenshot(self):
        logger.info("Taking a screenshot...")
