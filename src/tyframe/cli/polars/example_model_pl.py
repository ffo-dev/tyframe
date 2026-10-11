import polars as pl
from _tyframe_class_finder_183346278819788635 import ExampleModel
from tyframe.typed_df.typed_dfs import TypedPolarsDataFrame
class ExampleModelPl(TypedPolarsDataFrame[ExampleModel]):
    model: type[ExampleModel] = ExampleModel
    name: str = "name"
    last_name: str = "last_name"
    result: str = "result"
    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]
    @property
    def last_name_col(self) -> pl.Series:
        return self._df[self.last_name]
    @property
    def result_col(self) -> pl.Series:
        return self._df[self.result]