from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

from tyframe.base_df_model import BaseDfModel
from tyframe.validation.column_validation.column_validation import (
    get_extra_columns,
    get_missing_columns,
)
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.exceptions.column_exceptions import (
    ExtraColumnsError,
    MissingColumnsError,
    MissingColumnsWithoutDefaultError,
)

DataFrameType = TypeVar("DataFrameType")


class BaseValidator[DataFrameType](metaclass=ABCMeta):
    def __init__(
        self,
    ):
        # Currently the init is empty, configurations are explictly passed
        # to the validate method.
        # Left here in case some specialized validator needs
        # to have some configuration in the future.
        pass

    df_type: type[DataFrameType]

    def validate(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        config: TyframeValidationConfig | None = None,
    ) -> DataFrameType:
        if config is None:
            config = TyframeValidationConfig()
        res = self.validate_column_names(
            df_model,
            df,
            fill_with_default=config.fill_with_default,
            drop_extra=config.drop_extra_columns,
        )
        return res

    def validate_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        fill_with_default: bool,
        drop_extra: bool,
    ) -> DataFrameType:
        df = self.validate_missing_column_names(
            df_model,
            df,
            fill_with_default=fill_with_default,
        )
        df = self.validate_extra_column_names(
            df_model,
            df,
            drop_extra=drop_extra,
        )
        return df

    def create_dataframe(
        self,
        models: Iterable[BaseDfModel],
        model_type: type[BaseDfModel],
    ) -> DataFrameType:
        return self._create_dataframe_from_records(
            (el.to_record() for el in models),
            model_type,
        )

    @abstractmethod
    def _create_dataframe_from_records(
        self,
        records: Iterable[Mapping[str, Any]],  # pyright:ignore[reportExplicitAny]
        model_type: type[BaseDfModel],
    ) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_df_columns(self, df: DataFrameType) -> set[str]:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def drop_df_columns(
        self, df: DataFrameType, columns: Iterable[str]
    ) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def fill_defaults(
        self,
        df: DataFrameType,
        defaults: Mapping[str, Any],  # pyright:ignore[reportExplicitAny]
        missing_columns: set[str],
    ) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover

    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        fill_with_default: bool,
    ) -> DataFrameType:
        expected_columns = df_model.columns
        df_columns = self.get_df_columns(df)
        missing_columns = get_missing_columns(
            expected=expected_columns,
            df_columns=df_columns,
        )
        if missing_columns:
            if not fill_with_default:
                raise MissingColumnsError(
                    expected_columns=expected_columns,
                    missing_columns=missing_columns,
                )
            if missing_defaults := (missing_columns - df_model.defaults.keys()):
                raise MissingColumnsWithoutDefaultError(
                    missing_columns=missing_columns,
                    missing_without_default=missing_defaults,
                )
            df = self.fill_defaults(
                df,
                df_model.defaults,
                missing_columns,
            )

        return df

    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        drop_extra: bool,
    ) -> DataFrameType:
        expected_columns = df_model.columns
        df_columns = self.get_df_columns(df)
        extra_columns = get_extra_columns(
            expected=expected_columns,
            df_columns=df_columns,
        )

        if extra_columns:
            if not drop_extra:
                raise ExtraColumnsError(
                    expected_columns=expected_columns,
                    extra=extra_columns,
                )
            df = self.drop_df_columns(df, extra_columns)

        return df
