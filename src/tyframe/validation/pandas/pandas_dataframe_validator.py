from collections.abc import Iterable, Mapping
from typing import Any, override

from pandas import DataFrame

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.config import TyframeColumnValidation
from tyframe.validation.dtype_mapping import PandasDtypeMapping


class PandasValidator(BaseValidator[DataFrame]):
    def __init__(
        self,
        dtype_mapping: PandasDtypeMapping | None = None,
        config: TyframeColumnValidation | None = None,
    ) -> None:
        super().__init__(
            dtype_mapping=dtype_mapping or PandasDtypeMapping(),
            config=config,
        )

    df_type: type[DataFrame] = DataFrame

    @override
    def get_df_columns(
        self,
        df: DataFrame,
    ) -> set[str]:
        return set(df.columns)

    @override
    def drop_df_columns(
        self,
        df: DataFrame,
        columns: Iterable[str],
    ) -> DataFrame:
        return df.drop(columns=columns)

    @override
    def fill_defaults(
        self,
        df: DataFrame,
        defaults: Mapping[str, Any],  # pyright:ignore[reportExplicitAny]
        missing_columns: set[str],
    ) -> DataFrame:
        for col in missing_columns:
            df[col] = defaults[col]
        return df

    @override
    def get_df_dtype(self, df: DataFrame, column: str) -> Any:
        return df[column].dtype

    @override
    def _create_dataframe_from_records(
        self,
        records: Iterable[Mapping[str, Any]],  # pyright:ignore[reportExplicitAny]
        model_type: type[BaseDfModel],
    ) -> DataFrame:
        return DataFrame.from_records(records)
