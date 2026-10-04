from abc import ABCMeta
from collections.abc import Iterable, Mapping
from typing import Any, TypeVar, override

import polars as pl
from polars import DataFrame, LazyFrame

from tyframe.validation.base_validator import BaseValidator

PolarsDataFrameType = TypeVar("PolarsDataFrameType", DataFrame, LazyFrame)


class BasePolarsValidator[PolarsDataFrameType](
    BaseValidator[PolarsDataFrameType], metaclass=ABCMeta
):
    @override
    def drop_df_columns(
        self,
        df: PolarsDataFrameType,
        columns: Iterable[str],
    ) -> PolarsDataFrameType:
        return df.drop(columns)  # pyright:ignore[reportUnknownVariableType,reportUnknownVariableType,reportAttributeAccessIssue,reportUnknownMemberType]


class PolarsValidator(BasePolarsValidator[DataFrame]):
    @override
    def get_df_columns(self, df: DataFrame) -> set[str]:
        return set(df.columns)

    @override
    def fill_defaults(
        self,
        df: DataFrame,
        defaults: Mapping[str, Any],  # pyright:ignore[reportExplicitAny]
        missing_columns: set[str],
    ) -> DataFrame:
        cols = [pl.lit(defaults[key]).alias(key) for key in missing_columns]
        return df.with_columns(cols)


class LazyPolarsValidator(BasePolarsValidator[LazyFrame]):
    @override
    def get_df_columns(self, df: LazyFrame) -> set[str]:
        return set(df.collect_schema().names())

    @override
    def fill_defaults(
        self,
        df: LazyFrame,
        defaults: Mapping[str, Any],  # pyright:ignore[reportExplicitAny]
        missing_columns: set[str],
    ) -> LazyFrame:
        cols = [pl.lit(defaults[key]).alias(key) for key in missing_columns]
        return df.with_columns(cols)
