import pandas as pd
from benchmark.source_classes.models import C1
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class C1Pd(TypedPandasDataFrame[C1]):
    model: type[C1] = C1
    c_1: str = 'c_1'

    @property
    def c_1_col(self) -> pd.Series:
        return self._df[self.c_1]


#### CODE-GEN END
