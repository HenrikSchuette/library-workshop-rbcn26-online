from robotlibcore import DynamicCore
import requests

from robot.api.deco import library
from robot.api.interfaces import (
    Arguments,
)
from .models.openapi_rf_keyword_model import parse_openapi_spec
from .openapi_keyword_runner import OpenAPIKeywordRunner


@library
class OpenApiLibrary(DynamicCore):
    def __init__(self, base_url="http://localhost:8000"):
        super().__init__([])
        self.base_url = base_url
        open_api_spec = requests.get(f"{self.base_url}/openapi.json").json()
        self.open_api_rf_keywords = parse_openapi_spec(open_api_spec)

    def get_keyword_names(self):
        return list(self.open_api_rf_keywords.keys())

    def get_keyword_arguments(self, name) -> Arguments | None:
        open_api_keyword = self.open_api_rf_keywords.get(name)
        if not open_api_keyword:
            raise ValueError(f"Keyword '{name}' not found in OpenAPI specification.")
        arguments = [param.name for param in open_api_keyword.parameters]
        arguments.append("*")
        arguments.extend(list(open_api_keyword.request_body.keys()))
        return arguments

    def run_keyword(self, name, args, kwargs):
        open_api_keyword = self.open_api_rf_keywords.get(name)
        return OpenAPIKeywordRunner(open_api_keyword, self.base_url).execute(
            args, kwargs
        )

    def get_keyword_tags(self, name):
        return []

    def get_keyword_documentation(self, name):
        if name == "__intro__":
            return (
                "This library dynamically generates keywords based on the OpenAPI"
                " specification of the API. Each keyword corresponds to an API endpoint"
                " and allows you to interact with it directly from your Robot Framework tests."
            )
        if not self.open_api_rf_keywords.get(name):
            raise ValueError(f"Keyword '{name}' not found in OpenAPI specification.")
        return self.open_api_rf_keywords.get(name).method_item.description or ""

    def get_keyword_types(self, name):
        return []

    def get_keyword_source(self, keyword_name):
        return None


if __name__ == "__main__":
    OpenApiLibrary()
