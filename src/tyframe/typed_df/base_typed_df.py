from abc import ABCMeta

from tyframe.validation.pandas.pandas_dataframe_validator import PandasValidator
from tyframe.validation.polars.polars_dataframe_validator import (
    LazyPolarsValidator,
    PolarsValidator,
)


class BaseTypedDf[
    ModelType,
    Validator: PolarsValidator | LazyPolarsValidator | PandasValidator,
](metaclass=ABCMeta):
    pass
