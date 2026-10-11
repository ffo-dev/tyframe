import pandas as pd
from _tyframe_class_finder_183346278819788635 import ExampleModel
from tyframe.typed_df.typed_dfs import TypedPandasDataFrame
class ExampleModelPd(TypedPandasDataFrame[ExampleModel]):
    model: type[ExampleModel] = ExampleModel
    name: str = "name"
    last_name: str = "last_name"
    result: str = "result"
    @property
    def name_col(self) -> pd.Series:
        return self._df[self.name]
    @property
    def last_name_col(self) -> pd.Series:
        return self._df[self.last_name]
    @property
    def result_col(self) -> pd.Series:
        return self._df[self.result]