"""Type stubs for pydantic_settings module."""

from typing import Any, Type, TypeVar

ModelT = TypeVar("ModelT")

class SettingsConfigDict(dict[str, Any]):
    """Configuration dictionary for Pydantic Settings."""

    ...

class BaseSettings:
    """Base class for Pydantic settings with environment variable support."""

    model_config: SettingsConfigDict

    def __init__(self, **data: Any) -> None: ...
    @classmethod
    def model_validate_json(cls: Type[ModelT], json_data: str | bytes) -> ModelT: ...
    @classmethod
    def model_validate(cls: Type[ModelT], obj: Any) -> ModelT: ...
    def model_dump(self, **kwargs: Any) -> dict[str, Any]: ...
    def model_dump_json(self, **kwargs: Any) -> str: ...
