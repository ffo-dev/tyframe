from abc import ABCMeta
from collections.abc import Iterable
from typing import override

from polars import DataFrame, LazyFrame

from tyframe.validation.base_validator import BaseValidator

# TODO: create a base POlars validator that accept both options
PolarsDataframeType = DataFrame | LazyFrame


class BasePolarsValidator[PolarsDataframeType](
    BaseValidator[PolarsDataframeType], metaclass=ABCMeta
):
    @override
    def drop_df_columns(
        self,
        df: PolarsDataframeType,
        columns: Iterable[str],
    ) -> PolarsDataframeType:
        return df.drop(list(columns))


class PolarsValidator(BasePolarsValidator[DataFrame]):
    @override
    def get_df_columns(self, df: DataFrame) -> set[str]:
        return set(df.columns)


class LazyPolarsValidator(BasePolarsValidator[LazyFrame]):
    @override
    def get_df_columns(self, df: LazyFrame) -> set[str]:
        return set(df.collect_schema().names())
