from robotlibcore import keyword, DynamicCore
from request_keywords import RequestKeywords
from robot.api import logger


class TodoLibrary(DynamicCore):
    def __init__(self, timeout: int = 5, retry_on_failure: bool = True):
        super().__init__([RequestKeywords(self)])
        self.base_url = "http://localhost:8000"
        self.timeout = timeout
        self.retry_on_failure = retry_on_failure

    def run_keyword(self, name, args, kwargs=None):
        try:
            return super().run_keyword(name, args, kwargs)
        except Exception as e:
            if self.retry_on_failure:
                logger.warn(f"Keyword '{name}' failed. Retrying once...")
                return super().run_keyword(name, args, kwargs)
            raise e
