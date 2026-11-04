import pandas as pd
from tests.test_classes.models import TwoColModel
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


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
