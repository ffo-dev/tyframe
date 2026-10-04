from abc import ABCMeta
from typing import Any, ClassVar, override

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType


class BaseDfModel(BaseModel, metaclass=ABCMeta):
    """Base class to create a model to validate and build dataframes."""

    columns: ClassVar[list[str]]
    defaults: ClassVar[dict[str, Any]]  # pyright:ignore[reportExplicitAny]

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:  # pyright:ignore[reportExplicitAny, reportAny]
        cls.columns = list(cls.model_fields.keys())
        cls.defaults = {
            k: v.default  # pyright:ignore[reportAny]
            for k, v in cls.model_fields.items()
            if not isinstance(v.default, PydanticUndefinedType)  # pyright:ignore[reportAny]
        }
        super().__pydantic_init_subclass__(**kwargs)
