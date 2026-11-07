from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

from tyframe.base_df_model import BaseDfModel
from tyframe.validation.column_validation.column_validation import (
    get_extra_columns,
    get_missing_columns,
)
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.dtype_mapping import DtypeMapping, DtypeMismatchError
from tyframe.validation.exceptions.column_exceptions import (
    ExtraColumnsError,
    MissingColumnsError,
    MissingColumnsWithoutDefaultError,
)

DataFrameType = TypeVar('DataFrameType')


class BaseValidator[DataFrameType](metaclass=ABCMeta):
    def __init__(
        self,
        dtype_mapping: DtypeMapping[Any],
        config: TyframeValidationConfig | None = None,
    ) -> None:
        """Initialize the validator with an optional dtype mapping.

        Args:
            dtype_mapping: Optional dtype mapping for type validation.
                          If None, uses the default from the class.
        """
        self.dtype_mapping: DtypeMapping[Any] = dtype_mapping
        self.config = config or TyframeValidationConfig()

    df_type: type[DataFrameType]
    config: TyframeValidationConfig

    def validate(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
    ) -> DataFrameType:
        res = self.validate_column_names(
            df_model,
            df,
        )
        if self.config.validate_dtypes:
            res = self.validate_dtypes(df_model, res)
        return res

    def validate_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
    ) -> DataFrameType:
        df = self.validate_missing_column_names(
            df_model,
            df,
        )
        return self.validate_extra_column_names(
            df_model,
            df,
        )

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
        self,
        df: DataFrameType,
        columns: Iterable[str],
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
    ) -> DataFrameType:
        expected_columns = df_model.columns
        df_columns = self.get_df_columns(df)
        missing_columns = get_missing_columns(
            expected=expected_columns,
            df_columns=df_columns,
        )
        if missing_columns:
            if not self.config.fill_with_default:
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
    ) -> DataFrameType:
        expected_columns = df_model.columns
        df_columns = self.get_df_columns(df)
        extra_columns = get_extra_columns(
            expected=expected_columns,
            df_columns=df_columns,
        )

        if extra_columns:
            if not self.config.drop_extra_columns:
                raise ExtraColumnsError(
                    expected_columns=expected_columns,
                    extra=extra_columns,
                )
            df = self.drop_df_columns(df, extra_columns)

        return df

    @abstractmethod
    def get_df_dtype(self, df: DataFrameType, column: str) -> object:
        """Get the dtype of a column from the dataframe."""
        raise NotImplementedError  # pragma: no cover

    def validate_dtypes(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
    ) -> DataFrameType:
        """Validate that dataframe column dtypes match expected Pydantic types.

        Args:
            df_model: The Pydantic model defining expected types.
            df: The dataframe to validate.

        Returns:
            The validated dataframe (unchanged if validation passes).

        Raises:
            DtypeMismatchError: If a column dtype doesn't match the expected Pydantic type.
            PyTypeNotFoundError: If the expected Python type is not found in the mapping.
            DtypeNotFoundError: If the dataframe dtype is not found in the mapping.
        """
        for column in df_model.columns:
            df_dtype = self.get_df_dtype(df, column)
            expected_py_type = df_model.model_fields[column].annotation
            if expected_py_type is None:
                continue
            # Get all dataframe dtypes that map to the expected Python type
            valid_dtypes = self.dtype_mapping.get_dtypes(expected_py_type)
            if df_dtype not in valid_dtypes:
                raise DtypeMismatchError(column, df_dtype, expected_py_type, set(valid_dtypes))
        return df
