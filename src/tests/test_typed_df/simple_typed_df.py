import pandas as pd
import polars as pl

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.typed_df.typed_dfs import TypedPandasDataFrame, TypedPolarsDataFrame


class OneColModel(BaseDfModel):
    a: int


class TwoColModel(OneColModel):
    b: str


class OtherExample(BaseDfModel):
    yaba: str


class OneColModelPl(TypedPolarsDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel

    a: str = 'a'

    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]


class TwoColModelPl(TypedPolarsDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel

    a: str = 'a'
    b: str = 'b'

    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]

    @property
    def b_col(self) -> pl.Series:
        return self._df[self.b]


class OneColModelPd(TypedPandasDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel

    a: str = 'a'

    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]


class TwoColModelPd(TypedPandasDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel

    a: str = 'a'
    b: str = 'b'

    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]

    @property
    def b_col(self) -> pd.Series:
        return self._df[self.b]
