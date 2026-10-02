from abc import ABCMeta
from typing import Any, ClassVar, override

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType


class BaseDfModel(BaseModel, metaclass=ABCMeta):
    """Base class to create a model to validate and build dataframes."""

    columns: ClassVar[list[str]]
    column_defaults: ClassVar[dict[str, Any]]

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        cls.columns = list(cls.model_fields.keys())
        cls.column_defaults = {
            k: v.default
            for k, v in cls.model_fields.items()
            if not isinstance(v.default, PydanticUndefinedType)
        }
        super().__pydantic_init_subclass__(**kwargs)
