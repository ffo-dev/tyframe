import pandas as pd
from _tyframe_class_finder_6612836486764583728 import OtherExampleModel
from tyframe.typed_df.typed_dfs import TypedPandasDataFrame
class OtherExampleModelPd(TypedPandasDataFrame[OtherExampleModel]):
    model: type[OtherExampleModel] = OtherExampleModel
    name: str = "name"
    @property
    def name_col(self) -> pd.Series:
        return self._df[self.name]