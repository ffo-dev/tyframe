import polars as pl

from benchmark.source_classes.models import C1
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class C1Pl(TypedPolarsDataFrame[C1]):
    model: type[C1] = C1
    c_1: str = 'c_1'

    @property
    def c_1_col(self) -> pl.Series:
        return self._df[self.c_1]


#### CODE-GEN END
