from robotlibcore import keyword, DynamicCore
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class MyLibCoreLibrary(DynamicCore):
    def __init__(self, run_on_failure=None):
        super().__init__([])
        self.run_on_failure_keyword = run_on_failure

    def run_keyword(self, name, args, kwargs=None):
        try:
            return super().run_keyword(name, args, kwargs)
        except Exception as e:
            if self.run_on_failure_keyword:
                BuiltIn().run_keyword(self.run_on_failure_keyword)
            raise e

    @keyword
    def my_keyword(self):
        logger.info("Executing my_keyword...")

    @keyword
    def my_failing_keyword(self):
        raise Exception("This keyword always fails.")

    @keyword
    def take_screenshot(self):
        logger.info("Taking a screenshot...")
