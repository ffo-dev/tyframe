from abc import ABCMeta, abstractmethod
from typing import TypeVar

from tyframe.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig

DataFrameType = TypeVar("DataFrameType")


class BaseValidator[DataFrameType](metaclass=ABCMeta):

    def __init__(
        self,
    ):
        # Currently the init is empty, configurations are explictly passed
        # to the validate method.
        pass

    def validate(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        config: TyframeValidationConfig
    ) -> DataFrameType:
        res = self.validate_column_names(
            df_model,
            df,
            fill_with_default=config.fill_with_default,
            drop_extra=config.drop_extra_columns
        )
        return res

    def validate_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        fill_with_default: bool,
        drop_extra: bool
    ) -> DataFrameType:
        df = self.validate_missing_column_names(
            df_model,
            df,
            fill_with_default=fill_with_default
        )
        df = self.validate_extra_column_names(
            df_model,
            df,
            drop_extra=drop_extra
        )
        return df

    @abstractmethod
    def validate_missing_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        fill_with_default: bool
    ) -> DataFrameType:
        raise NotImplementedError

    @abstractmethod
    def validate_extra_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        drop_extra: bool
    ) -> DataFrameType:
        raise NotImplementedError
    