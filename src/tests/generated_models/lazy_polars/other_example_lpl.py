import polars as pl

from tests.test_classes.models import OtherExample
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame


#### CODE-GEN START
class OtherExampleLpl(TypedLazyPolarsDataFrame[OtherExample]):
    model: type[OtherExample] = OtherExample
    yaba: str = 'yaba'

    @property
    def yaba_col(self) -> pl.Series:
        return self._df.select(self.yaba).collect().to_series()


#### CODE-GEN END
