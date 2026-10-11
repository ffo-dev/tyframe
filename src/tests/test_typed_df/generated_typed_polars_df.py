import polars as pl

from tests.test_typed_df.simple_typed_df import TwoColModel
from tyframe.typed_df.typed_dfs import TypedPolarsDataFrame


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
