import polars as pl
from tests.test_classes.models import OneColModel
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


class OneColModelPl(TypedPolarsDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = 'a'

    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]
