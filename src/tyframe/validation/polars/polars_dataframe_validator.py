from collections.abc import Iterable, Mapping
from typing import Any, override

import polars as pl
from polars import DataFrame, LazyFrame

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.dtype_mapping import PolarsDtypeMapping


class PolarsValidator(BaseValidator[DataFrame]):
    df_type: type[DataFrame] = DataFrame

    def __init__(
        self,
        dtype_mapping: PolarsDtypeMapping | None = None,
        config: TyframeValidationConfig | None = None,
    ) -> None:
        super().__init__(
            dtype_mapping=dtype_mapping or PolarsDtypeMapping(),
            config=config,
        )

    @override
    def drop_df_columns(
        self,
        df: DataFrame,
        columns: Iterable[str],
    ) -> DataFrame:
        return df.drop(
            columns,
            strict=False,
        )

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

    @override
    def get_df_dtype(self, df: DataFrame, column: str) -> pl.DataType:
        return df.schema[column]

    @override
    def _create_dataframe_from_records(
        self,
        records: Iterable[Mapping[str, Any]],  # pyright:ignore[reportExplicitAny]
        model_type: type[BaseDfModel],
    ) -> DataFrame:
        return pl.DataFrame(records)


class LazyPolarsValidator(BaseValidator[LazyFrame]):
    df_type: type[LazyFrame] = LazyFrame

    def __init__(
        self,
        dtype_mapping: PolarsDtypeMapping | None = None,
        config: TyframeValidationConfig | None = None,
    ) -> None:
        super().__init__(
            dtype_mapping=dtype_mapping or PolarsDtypeMapping(),
            config=config,
        )

    @override
    def drop_df_columns(
        self,
        df: LazyFrame,
        columns: Iterable[str],
    ) -> LazyFrame:
        return df.drop(
            columns,
            strict=False,
        )

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

    @override
    def get_df_dtype(self, df: LazyFrame, column: str) -> pl.DataType:
        return df.collect_schema()[column]

    @override
    def _create_dataframe_from_records(
        self,
        records: Iterable[Mapping[str, Any]],  # pyright:ignore[reportExplicitAny]
        model_type: type[BaseDfModel],
    ) -> LazyFrame:
        return pl.LazyFrame(records)
