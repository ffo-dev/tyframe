import polars as pl

from tyframe.dummy.test_model import ExampleModel
from tyframe.typed_df.polars import TypedLazyPolarsDataFrame


class ExampleModelLpl(TypedLazyPolarsDataFrame[ExampleModel]):
    model: type[ExampleModel] = ExampleModel
    name: str = 'name'
    last_name: str = 'last_name'
    result: str = 'result'

    @property
    def name_col(self) -> pl.Series:
        return self._df.select(self.name).collect().to_series()

    @property
    def last_name_col(self) -> pl.Series:
        return self._df.select(self.last_name).collect().to_series()

    @property
    def result_col(self) -> pl.Series:
        return self._df.select(self.result).collect().to_series()
