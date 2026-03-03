from robotlibcore import keyword, DynamicCore
from request_keywords import RequestKeywords
from robot.api.deco import library


@library(scope="GLOBAL")
class TodoLibrary(DynamicCore):
    def __init__(self, timeout: int = 15):
        super().__init__([RequestKeywords(self)])
        self.base_url = "http://localhost:8000"
        self.timeout = timeout
