import polars as pl

from tests.test_classes.models import TaggedModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame


#### CODE-GEN START
class TaggedModelLpl(TypedLazyPolarsDataFrame[TaggedModel]):
    model: type[TaggedModel] = TaggedModel
    id: str = 'id'
    price: str = 'price'
    country: str = 'country'
    name: str = 'name'

    @property
    def id_col(self) -> pl.Series:
        return self._df.select(self.id).collect().to_series()

    @property
    def price_col(self) -> pl.Series:
        return self._df.select(self.price).collect().to_series()

    @property
    def country_col(self) -> pl.Series:
        return self._df.select(self.country).collect().to_series()

    @property
    def name_col(self) -> pl.Series:
        return self._df.select(self.name).collect().to_series()

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
