from collections.abc import Iterable
from typing import override

from polars import DataFrame, LazyFrame

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.column_validation import get_extra_columns, get_missing_columns
from tyframe.validation.exceptions import ExtraColumnsError, MissingColumnsError

# TODO: create a base POlars validator that accept both options
PolarsDataframeType = DataFrame | LazyFrame

class BasePolarsValidator[PolarsDataframeType](BaseValidator[PolarsDataframeType]):

    @override
    def drop_df_columns(
        self,
        df: PolarsDataframeType,
        columns: Iterable[str]
    ) -> PolarsDataframeType:
        return df.drop(list(columns))

class PolarsValidator(BasePolarsValidator[DataFrame]):

    @override
    def get_df_columns(
        self,
        df: DataFrame
    ) -> set[str]:
        return set(df.columns)


class LazyPolarsValidator(BasePolarsValidator[LazyFrame]):
    @override
    def get_df_columns(
        self,
        df: LazyFrame
    ) -> set[str]:
        return set(df.collect_schema().names())