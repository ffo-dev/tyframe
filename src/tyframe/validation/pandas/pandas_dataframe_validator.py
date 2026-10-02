from typing import override

from pandas import DataFrame

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.column_validation import get_extra_columns, get_missing_columns
from tyframe.validation.exceptions import ExtraColumnsError, MissingColumnsError


class PandasValidator(BaseValidator[DataFrame]):
    @override
    def validate_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrame,
        *,
        drop_extra_columns: bool,
    ) -> DataFrame:
        expected_columns = df_model.columns
        df_columns = list(df.columns)
        missing_columns = get_missing_columns(
            expected=expected_columns, df_columns=df_columns
        )
        if missing_columns:
            raise MissingColumnsError(
                expected_columns=expected_columns, missing_columns=missing_columns
            )

        extra_columns = get_extra_columns(
            expected=expected_columns, df_columns=df_columns
        )

        if extra_columns:
            if not drop_extra_columns:
                raise ExtraColumnsError(
                    expected_columns=expected_columns, extra=extra_columns
                )
            df = df.drop(columns=list(extra_columns))

        return df
