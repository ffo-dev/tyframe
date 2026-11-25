from abc import ABCMeta
from collections.abc import Callable
from typing import Any, Self, override

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

    def __and__(self, other: Self) -> Self:
        return self._combine(other, lambda a, b: a and b)

    def __or__(self, other: Self) -> Self:
        return self._combine(other, lambda a, b: a or b)

    def _combine(self, other: Self, op: Callable[[bool, bool], bool]) -> Self:
        if not isinstance(other, BaseTyframeValidationConfig):  # pyright:ignore[reportUnnecessaryIsInstance]
            return NotImplemented
        combined = {
            name: op(bool(getattr(self, name)), bool(getattr(other, name, False))) for name in type(self).model_fields
        }
        return type(self)(**combined)


class TyframeValidationConfig(BaseTyframeValidationConfig):
    drop_extra_columns: bool = Field(default=False)
    fill_with_default: bool = Field(default=False)
    validate_dtypes: bool = Field(default=False)
