import polars as pl

from tests.test_classes.models import OneColModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame


#### CODE-GEN START
class OneColModelLpl(TypedLazyPolarsDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = 'a'

    @property
    def a_col(self) -> pl.Series:
        return self._df.select(self.a).collect().to_series()

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
