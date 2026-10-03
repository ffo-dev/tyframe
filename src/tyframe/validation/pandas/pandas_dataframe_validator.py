from typing import override

from pandas import DataFrame

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator
from tyframe.validation.column_validation import get_extra_columns, get_missing_columns
from tyframe.validation.exceptions import (
    ExtraColumnsError,
    MissingColumnsError,
    MissingColumnsWithoutDefaultError,
)


class PandasValidator(BaseValidator[DataFrame]):

    @override
    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrame,
        *,
        fill_with_default: bool
    ) -> DataFrame:
        expected_columns = df_model.columns
        df_columns = set(df.columns)
        missing_columns = get_missing_columns(
            expected=expected_columns, df_columns=df_columns,
        )
        if missing_columns:
            if not fill_with_default:
                raise MissingColumnsError(
                expected_columns=expected_columns, missing_columns=missing_columns
            )
            if missing_defaults := (missing_columns - df_model.defaults.keys()):
                MissingColumnsWithoutDefaultError(
                    missing_columns=missing_columns,
                    missing_defaults=missing_defaults
                )
            for col in missing_columns:
                df[col] = df_model.defaults[col]
            
                 
        return df

    @override
    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrame,
        *,
        drop_extra: bool
    ) -> DataFrame:
        expected_columns = df_model.columns
        df_columns = list(df.columns)
        extra_columns = get_extra_columns(
            expected=expected_columns, df_columns=df_columns
        )

        if extra_columns:
            if not drop_extra:
                raise ExtraColumnsError(
                    expected_columns=expected_columns, extra=extra_columns
                )
            df = df.drop(columns=list(extra_columns))

        return df