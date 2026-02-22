"""Generic dataclass model for OpenAPI 3.1.0 specification."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Info:
    """OpenAPI Info Object."""

    title: str
    version: str
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[Dict[str, Any]] = None
    license: Optional[Dict[str, Any]] = None


@dataclass
class Schema:
    """OpenAPI Schema Object."""

    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, "Schema"]] = None
    items: Optional["Schema"] = None
    required: Optional[List[str]] = None
    enum: Optional[List[Any]] = None
    default: Optional[Any] = None
    anyOf: Optional[List["Schema"]] = None
    allOf: Optional[List["Schema"]] = None
    oneOf: Optional[List["Schema"]] = None
    ref: Optional[str] = field(default=None, metadata={"json_name": "$ref"})
    additionalProperties: Optional[Any] = None
    format: Optional[str] = None
    pattern: Optional[str] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    minItems: Optional[int] = None
    maxItems: Optional[int] = None


@dataclass
class MediaType:
    """OpenAPI Media Type Object."""

    schema: Optional[Schema] = None
    example: Optional[Any] = None
    examples: Optional[Dict[str, Any]] = None


@dataclass
class Response:
    """OpenAPI Response Object."""

    description: str
    content: Optional[Dict[str, MediaType]] = None
    headers: Optional[Dict[str, Any]] = None


@dataclass
class RequestBody:
    """OpenAPI Request Body Object."""

    content: Dict[str, MediaType]
    required: bool = False
    description: Optional[str] = None


@dataclass
class Parameter:
    """OpenAPI Parameter Object."""

    name: str
    location: str = field(metadata={"json_name": "in"})
    schema: Optional[Schema] = None
    required: bool = False
    description: Optional[str] = None
    deprecated: bool = False
    allowEmptyValue: bool = False


@dataclass
class Operation:
    """OpenAPI Operation Object (GET, POST, PUT, DELETE, etc)."""

    summary: Optional[str] = None
    description: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Parameter]] = None
    requestBody: Optional[RequestBody] = None
    responses: Dict[str, Response] = field(default_factory=dict)
    tags: Optional[List[str]] = None
    deprecated: bool = False
    security: Optional[List[Dict[str, List[str]]]] = None


@dataclass
class PathItem:
    """OpenAPI Path Item Object."""

    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    parameters: Optional[List[Parameter]] = None
    description: Optional[str] = None
    summary: Optional[str] = None


@dataclass
class Components:
    """OpenAPI Components Object."""

    schemas: Optional[Dict[str, Schema]] = None
    responses: Optional[Dict[str, Response]] = None
    parameters: Optional[Dict[str, Parameter]] = None
    requestBodies: Optional[Dict[str, RequestBody]] = None
    securitySchemes: Optional[Dict[str, Any]] = None


@dataclass
class OpenAPI:
    """Root OpenAPI Document Object."""

    openapi: str
    info: Info
    paths: Dict[str, PathItem] = field(default_factory=dict)
    components: Optional[Components] = None
    servers: Optional[List[Dict[str, Any]]] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Dict[str, Any]]] = None
    externalDocs: Optional[Dict[str, Any]] = None


# Parser functions


def parse_schema(data: Optional[Dict[str, Any]]) -> Optional[Schema]:
    """Parse JSON data into Schema object."""
    if data is None:
        return None

    return Schema(
        type=data.get("type"),
        title=data.get("title"),
        description=data.get("description"),
        properties={k: parse_schema(v) for k, v in data.get("properties", {}).items()}
        if data.get("properties")
        else None,
        items=parse_schema(data.get("items")) if data.get("items") else None,
        required=data.get("required"),
        enum=data.get("enum"),
        default=data.get("default"),
        anyOf=[parse_schema(s) for s in data.get("anyOf", [])]
        if data.get("anyOf")
        else None,
        allOf=[parse_schema(s) for s in data.get("allOf", [])]
        if data.get("allOf")
        else None,
        oneOf=[parse_schema(s) for s in data.get("oneOf", [])]
        if data.get("oneOf")
        else None,
        ref=data.get("$ref"),
        additionalProperties=data.get("additionalProperties"),
        format=data.get("format"),
        pattern=data.get("pattern"),
        minimum=data.get("minimum"),
        maximum=data.get("maximum"),
        minLength=data.get("minLength"),
        maxLength=data.get("maxLength"),
        minItems=data.get("minItems"),
        maxItems=data.get("maxItems"),
    )


def parse_media_type(data: Optional[Dict[str, Any]]) -> Optional[MediaType]:
    """Parse JSON data into MediaType object."""
    if data is None:
        return None

    return MediaType(
        schema=parse_schema(data.get("schema")),
        example=data.get("example"),
        examples=data.get("examples"),
    )


def parse_response(data: Dict[str, Any]) -> Response:
    """Parse JSON data into Response object."""
    return Response(
        description=data["description"],
        content={k: parse_media_type(v) for k, v in data.get("content", {}).items()}
        if data.get("content")
        else None,
        headers=data.get("headers"),
    )


def parse_request_body(data: Optional[Dict[str, Any]]) -> Optional[RequestBody]:
    """Parse JSON data into RequestBody object."""
    if data is None:
        return None

    return RequestBody(
        content={k: parse_media_type(v) for k, v in data["content"].items()},
        required=data.get("required", False),
        description=data.get("description"),
    )


def parse_parameter(data: Dict[str, Any]) -> Parameter:
    """Parse JSON data into Parameter object."""
    return Parameter(
        name=data["name"],
        location=data["in"],
        schema=parse_schema(data.get("schema")),
        required=data.get("required", False),
        description=data.get("description"),
        deprecated=data.get("deprecated", False),
        allowEmptyValue=data.get("allowEmptyValue", False),
    )


def parse_operation(data: Optional[Dict[str, Any]]) -> Optional[Operation]:
    """Parse JSON data into Operation object."""
    if data is None:
        return None

    return Operation(
        summary=data.get("summary"),
        description=data.get("description"),
        operationId=data.get("operationId"),
        parameters=[parse_parameter(p) for p in data.get("parameters", [])],
        requestBody=parse_request_body(data.get("requestBody")),
        responses={k: parse_response(v) for k, v in data.get("responses", {}).items()},
        tags=data.get("tags"),
        deprecated=data.get("deprecated", False),
        security=data.get("security"),
    )


def parse_path_item(data: Dict[str, Any]) -> PathItem:
    """Parse JSON data into PathItem object."""
    return PathItem(
        get=parse_operation(data.get("get")),
        put=parse_operation(data.get("put")),
        post=parse_operation(data.get("post")),
        delete=parse_operation(data.get("delete")),
        options=parse_operation(data.get("options")),
        head=parse_operation(data.get("head")),
        patch=parse_operation(data.get("patch")),
        trace=parse_operation(data.get("trace")),
        parameters=[parse_parameter(p) for p in data.get("parameters", [])]
        if data.get("parameters")
        else None,
        description=data.get("description"),
        summary=data.get("summary"),
    )


def parse_components(data: Optional[Dict[str, Any]]) -> Optional[Components]:
    """Parse JSON data into Components object."""
    if data is None:
        return None

    return Components(
        schemas={k: parse_schema(v) for k, v in data.get("schemas", {}).items()}
        if data.get("schemas")
        else None,
        responses={k: parse_response(v) for k, v in data.get("responses", {}).items()}
        if data.get("responses")
        else None,
        parameters={
            k: parse_parameter(v) for k, v in data.get("parameters", {}).items()
        }
        if data.get("parameters")
        else None,
        requestBodies={
            k: parse_request_body(v) for k, v in data.get("requestBodies", {}).items()
        }
        if data.get("requestBodies")
        else None,
        securitySchemes=data.get("securitySchemes"),
    )


def parse_info(data: Dict[str, Any]) -> Info:
    """Parse JSON data into Info object."""
    return Info(
        title=data["title"],
        version=data["version"],
        description=data.get("description"),
        termsOfService=data.get("termsOfService"),
        contact=data.get("contact"),
        license=data.get("license"),
    )


def parse_openapi(data: Dict[str, Any]) -> OpenAPI:
    """Parse JSON data into OpenAPI object."""
    return OpenAPI(
        openapi=data["openapi"],
        info=parse_info(data["info"]),
        paths={k: parse_path_item(v) for k, v in data.get("paths", {}).items()},
        components=parse_components(data.get("components")),
        servers=data.get("servers"),
        security=data.get("security"),
        tags=data.get("tags"),
        externalDocs=data.get("externalDocs"),
    )


def parse_openapi_json(json: Path) -> OpenAPI:
    with open(json, "r") as f:
        json_data = f.read()
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    return parse_openapi(data)
