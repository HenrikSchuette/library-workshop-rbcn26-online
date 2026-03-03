from robotlibcore import keyword, DynamicCore
from request_keywords import RequestKeywords


class TodoLibrary(DynamicCore):
    def __init__(self):
        super().__init__([RequestKeywords()])
        # self.base_url = "http://localhost:8000"
