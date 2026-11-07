import polars as pl
from tests.test_classes.models import OtherExample
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


class OtherExamplePl(TypedPolarsDataFrame[OtherExample]):
    model: type[OtherExample] = OtherExample
    yaba: str = 'yaba'
    @property
    def yaba_col(self) -> pl.Series:
        return self._df[self.yaba]
