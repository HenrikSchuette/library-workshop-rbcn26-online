from pathlib import Path

from robotlibcore import PluginParser, keyword, DynamicCore
from request_keywords import RequestKeywords
from robot.api import logger
from library_component import BaseLibraryComponent


class TodoLibrary(DynamicCore):
    def __init__(
        self,
        translation: Path,
        plugin: Path,
        timeout: int = 5,
        retry_on_failure: bool = True,
    ):
        library_components = PluginParser(BaseLibraryComponent, [self]).parse_plugins(
            plugin.as_posix()
        )
        library_components.append(RequestKeywords(self))
        super().__init__(library_components, translation=translation.absolute())
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
            else:
                raise e
