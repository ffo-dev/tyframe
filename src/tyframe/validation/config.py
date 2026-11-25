from abc import ABCMeta
from typing import Any, override

from pydantic import BaseModel, Field


class BaseTyframeValidationConfig(BaseModel, metaclass=ABCMeta):
    """Base class for validation configuration.

    This class is intended to be subclassed to create specific validation configurations.
    Subclasses may only add boolean fields.
    """

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:  # pyright:ignore[reportExplicitAny, reportAny]
        non_bool_fields = [name for name, field_info in cls.model_fields.items() if field_info.annotation is not bool]
        if non_bool_fields:
            msg = f'{cls.__qualname__} may only add boolean fields; non-boolean fields: {", ".join(non_bool_fields)}'
            raise TypeError(msg)
        super().__pydantic_init_subclass__(**kwargs)


class TyframeValidationConfig(BaseTyframeValidationConfig):
    drop_extra_columns: bool = Field(default=False)
    fill_with_default: bool = Field(default=False)
    validate_dtypes: bool = Field(default=False)
