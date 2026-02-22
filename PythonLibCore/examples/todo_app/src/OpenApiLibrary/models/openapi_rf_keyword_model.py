# Robot Keyword Model


from dataclasses import dataclass
import re
from typing import Any, Dict
from OpenApiLibrary.models.openapi_model import (
    OpenAPI,
    Operation,
    PathItem,
    parse_openapi,
)


@dataclass
class OpenApiKeyword:
    name: str
    method: str
    method_item: Operation
    path: str
    parameters: list
    request_body: dict[str, dict]


def get_sanitized_keyword_name(method: str, path: str) -> str:
    keyword_name = f"{method} {path}"
    sanitized_keyword_name = re.sub(r"\{.*?\}", "", keyword_name)
    sanitized_keyword_name = (
        sanitized_keyword_name.replace("/", "").replace(" ", "_").lower()
    )
    return sanitized_keyword_name


def get_path_methods(path: PathItem) -> dict[str, Operation]:
    return {
        method: getattr(path, method)
        for method in ["get", "post", "put", "delete"]
        if getattr(path, method) is not None
    }


def get_path_method_iterator(
    open_api_model: OpenAPI,
) -> tuple[str, PathItem, str, Operation]:  # type: ignore
    for path_name, path_item in open_api_model.paths.items():
        if path_name == "/":
            continue
        method_items = get_path_methods(path_item)
        for method_name, method in method_items.items():
            yield path_name, path_item, method_name, method


def get_keyword_argument_schemas(method: Operation, open_api_model: OpenAPI):
    if (
        not method
        or not method.requestBody
        or not method.requestBody
        or not method.requestBody.content.get("application/json")
        or not method.requestBody.content["application/json"].schema
        or not method.requestBody.content["application/json"].schema.ref
    ):
        return {}
    ref = method.requestBody.content["application/json"].schema.ref.split("/")[-1]
    if ref:
        return {
            ref: {
                property_name: property_schema
                for property_name, property_schema in open_api_model.components.schemas[
                    ref
                ].properties.items()
            }
        }
    return {}


def parse_openapi_spec(data: Dict[str, Any]) -> dict[str, OpenApiKeyword]:
    keywords = {}
    open_api_model = parse_openapi(data)
    for path_name, _, method_name, method in get_path_method_iterator(open_api_model):
        keyword_name = get_sanitized_keyword_name(method_name, path_name)
        keywords[keyword_name] = OpenApiKeyword(
            name=keyword_name,
            method=method_name,
            method_item=method,
            path=path_name,
            parameters=method.parameters,
            request_body=get_keyword_argument_schemas(method, open_api_model),
        )
    return keywords
