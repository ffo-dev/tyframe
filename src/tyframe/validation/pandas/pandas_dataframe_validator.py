from collections.abc import Iterable
from typing import override

from pandas import DataFrame

from tyframe.validation.base_validator import BaseValidator


class PandasValidator(BaseValidator[DataFrame]):
    @override
    def get_df_columns(self, df: DataFrame) -> set[str]:
        return set(df.columns)

    @override
    def drop_df_columns(self, df: DataFrame, columns: Iterable[str]) -> DataFrame:
        return df.drop(columns=list(columns))
