from copy import copy
import re
from typing import Any

import requests  # type: ignore

from .models.openapi_rf_keyword_model import OpenApiKeyword


class OpenAPIKeywordRunner:
    def __init__(self, open_api_rf_keyword: OpenApiKeyword, base_url: str) -> None:
        self.open_api_rf_keyword = open_api_rf_keyword
        self.base_url = base_url

    def execute(self, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
        url = f"{self.base_url}{self.open_api_rf_keyword.path}"
        url, extra_keyword_args = self.format_url_with_kwargs(kwargs, url)
        url, _ = self.format_url_with_args(args, url)
        request_body = self.build_request_body(extra_keyword_args)
        response = requests.request(
            self.open_api_rf_keyword.method,
            url,
            json=request_body if request_body else None,
        )
        return self.build_result_from_response(response)

    def build_result_from_response(self, response: requests.Response) -> Any:
        if not response.ok:
            raise ValueError(response.text)
        try:
            response_json = response.json()
            if response_json:
                return response_json
        except ValueError:
            return None

    def build_request_body(self, extra_keyword_args: dict[str, Any]) -> Any:
        request_body = [
            extra_keyword_args.get(key)
            for key in self.open_api_rf_keyword.request_body.keys()
        ]
        if len(request_body) == 1:
            return request_body[0]
        return request_body

    def format_url_with_args(
        self, args: tuple[Any, ...], url: str
    ) -> tuple[str, list[Any]]:
        new_args = list(copy(args))
        for index, placeholder in enumerate(re.findall(r"\{.*?\}", url)):
            url = url.replace(placeholder, new_args.pop(index), count=1)
        return url, new_args

    def format_url_with_kwargs(
        self, kwargs: dict[str, Any], url: str
    ) -> tuple[str, dict[str, Any]]:
        new_kwargs = copy(kwargs)
        for kw_name, kw_value in kwargs.items():
            prev_url = url
            url = url.format(**{kw_name: kw_value})
            if prev_url != url:
                new_kwargs.pop(kw_name)
        return url, new_kwargs
