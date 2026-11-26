import polars as pl
from tests.test_classes.models import TaggedModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class TaggedModelPl(TypedPolarsDataFrame[TaggedModel]):
    model: type[TaggedModel] = TaggedModel
    id: str = 'id'
    price: str = 'price'
    country: str = 'country'
    name: str = 'name'

    @property
    def id_col(self) -> pl.Series:
        return self._df[self.id]

    @property
    def price_col(self) -> pl.Series:
        return self._df[self.price]

    @property
    def country_col(self) -> pl.Series:
        return self._df[self.country]

    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
