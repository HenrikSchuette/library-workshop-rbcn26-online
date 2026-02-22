from typing import Any

from robotlibcore import DynamicCore  # type: ignore
import requests  # type: ignore

from robot.api.deco import library
from robot.api.interfaces import (
    Arguments,
)
from .models.openapi_rf_keyword_model import parse_openapi_spec
from .openapi_keyword_runner import OpenAPIKeywordRunner


@library
class OpenApiLibrary(DynamicCore):
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        super().__init__([])
        self.base_url = base_url
        open_api_spec = requests.get(f"{self.base_url}/openapi.json").json()
        self.open_api_rf_keywords = parse_openapi_spec(open_api_spec)

    def get_keyword_names(self) -> list[str]:
        return list(self.open_api_rf_keywords.keys())

    def get_keyword_arguments(self, name) -> Arguments | None:
        open_api_keyword = self.open_api_rf_keywords.get(name)
        if not open_api_keyword:
            raise ValueError(f"Keyword '{name}' not found in OpenAPI specification.")
        arguments = [param.name for param in open_api_keyword.parameters]
        arguments.append("*")
        arguments.extend(list(open_api_keyword.request_body.keys()))
        return arguments

    def run_keyword(
        self, name: str, args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> Any:
        open_api_keyword = self.open_api_rf_keywords.get(name)
        if not open_api_keyword:
            raise ValueError(f"Keyword '{name}' not found in OpenAPI specification.")
        return OpenAPIKeywordRunner(open_api_keyword, self.base_url).execute(
            args, kwargs
        )

    def get_keyword_tags(self, name: str) -> list[str]:
        return []

    def get_keyword_documentation(self, name: str) -> str | None:
        if name == "__intro__":
            return (
                "This library dynamically generates keywords based on the OpenAPI"
                " specification of the API. Each keyword corresponds to an API endpoint"
                " and allows you to interact with it directly from your Robot Framework tests."
            )
        open_api_kw = self.open_api_rf_keywords.get(name)
        if not open_api_kw:
            raise ValueError(f"Keyword '{name}' not found in OpenAPI specification.")
        return open_api_kw.method_item.description or ""

    def get_keyword_types(self, name: str) -> list[Any]:
        return []

    def get_keyword_source(self, keyword_name: str) -> None:
        return None


if __name__ == "__main__":
    OpenApiLibrary()
