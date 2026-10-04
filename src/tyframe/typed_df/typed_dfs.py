from abc import ABCMeta
from typing import Self, TypeVar

import polars as pl

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.polars.polars_dataframe_validator import (
    PolarsValidator,
)

_T = TypeVar("_T", bound="TypedPolarsDataFrame")


class TypedPolarsDataFrame[
    ModelType: BaseDfModel,
](metaclass=ABCMeta):
    df: pl.DataFrame
    validator: PolarsValidator
    model: type[ModelType]

    def __init__(
        self,
        input_data: pl.DataFrame,
        validator: PolarsValidator,
        validation_config: TyframeValidationConfig | None = None,
    ):
        self.df = validator.validate(
            self.model,
            input_data,
            validation_config,
        )
        self.validator = validator

    @classmethod
    def columns(cls) -> list[str]:
        return list(cls.df.columns)

    def select(
        self,
        columns: list[str],
    ) -> pl.DataFrame:
        return self.df.select(columns)

    def select_to(
        self,
        to_type: type[_T],
    ) -> _T:
        return to_type(self.select(to_type.columns()), self.validator)

    def first(self) -> ModelType:
        return self.model(**self.df.head(n=1).to_dicts()[0])

    def collect(self) -> list[ModelType]:
        return [self.model(**row) for row in self.df.to_dicts()]

    def count(self) -> int:
        return self.df.height

    def distinct(self) -> Self:
        return type(self)(self.df.unique(), self.validator)

    def union(self, other: Self) -> Self:
        return type(self)(self.df.vstack(other.df), self.validator)
