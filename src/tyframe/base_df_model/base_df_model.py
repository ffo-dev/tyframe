from abc import ABCMeta
from typing import Any, ClassVar, override

from pydantic import BaseModel


class BaseDfModel(BaseModel, metaclass=ABCMeta):
    """Base class to create a model to validate and build dataframes."""

    columns: ClassVar[list[str]]

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        cls.columns = list(cls.model_fields.keys())

        super().__pydantic_init_subclass__(**kwargs)
