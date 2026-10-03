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
    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: PolarsDataframeType,
        *,
        fill_with_default: bool
    ) -> PolarsDataframeType:
        # TODO: actually reuse code more, but basedpyright complains about the union
        raise NotImplementedError  # pragma: no cover

    @override
    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: PolarsDataframeType,
        *,
        drop_extra: bool
    ) -> PolarsDataframeType:
        # TODO: actually reuse code more, but basedpyright complains about the union
        raise NotImplementedError  # pragma: no cover
    
class PolarsValidator(BasePolarsValidator[DataFrame]):

    @override
    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrame,
        *,
        fill_with_default: bool
    ) -> DataFrame:
        expected_columns = df_model.columns
        df_columns = df.columns
        missing_columns = get_missing_columns(
            expected=expected_columns, df_columns=df_columns
        )
        if missing_columns:
            raise MissingColumnsError(
                expected_columns=expected_columns, missing_columns=missing_columns
            )
        return df

    @override
    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: PolarsDataframeType,
        *,
        drop_extra: bool
    ) -> PolarsDataframeType:
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
            df = df.drop(list(extra_columns))

        return df


class LazyPolarsValidator(BasePolarsValidator[LazyFrame]):
    @override
    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrame,
        *,
        fill_with_default: bool
    ) -> DataFrame:
        expected_columns = df_model.columns
        df_columns = df.columns
        missing_columns = get_missing_columns(
            expected=expected_columns, df_columns=df_columns
        )
        if missing_columns:
            raise MissingColumnsError(
                expected_columns=expected_columns, missing_columns=missing_columns
            )
        return df

    @override
    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: PolarsDataframeType,
        *,
        drop_extra: bool
    ) -> PolarsDataframeType:
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
            df = df.drop(list(extra_columns))

        return df