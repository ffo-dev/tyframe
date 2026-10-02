from abc import ABCMeta, abstractmethod
from typing import TypeVar

from tyframe.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig

DataFrameType = TypeVar("DataFrameType")


class BaseValidator[DataFrameType](metaclass=ABCMeta):

    _config: TyframeValidationConfig

    def __init__(
        self,
        config: TyframeValidationConfig,
    ):
        self._config = config

    def validate(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
    ) -> DataFrameType:
        res = self.validate_column_names(
            df_model,
            df,
            drop_extra_columns=self._config.drop_extra_columns,
        )
        return res

    @abstractmethod
    def validate_column_names(
        self,
        df_model: type[BaseDfModel],
        df: DataFrameType,
        *,
        drop_extra_columns: bool,
    ) -> DataFrameType:
        raise NotImplementedError  # pragma: no cover
