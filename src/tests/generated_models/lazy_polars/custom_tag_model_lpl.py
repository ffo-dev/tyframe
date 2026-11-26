import polars as pl

from tests.test_classes.models import CustomTagModel, MyTag
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame


#### CODE-GEN START
class CustomTagModelLpl(TypedLazyPolarsDataFrame[CustomTagModel]):
    model: type[CustomTagModel] = CustomTagModel
    a: str = 'a'
    b: str = 'b'
    c: str = 'c'

    @property
    def a_col(self) -> pl.Series:
        return self._df.select(self.a).collect().to_series()

    @property
    def b_col(self) -> pl.Series:
        return self._df.select(self.b).collect().to_series()

    @property
    def c_col(self) -> pl.Series:
        return self._df.select(self.c).collect().to_series()

    @classmethod
    def columns_with_tag(cls, tag: MyTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
