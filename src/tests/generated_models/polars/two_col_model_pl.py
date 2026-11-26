import polars as pl
from tests.test_classes.models import TwoColModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class TwoColModelPl(TypedPolarsDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel
    a: str = 'a'
    b: str = 'b'

    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]

    @property
    def b_col(self) -> pl.Series:
        return self._df[self.b]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
