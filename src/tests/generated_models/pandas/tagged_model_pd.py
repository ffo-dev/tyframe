from typing import Literal

import pandas as pd
from tests.test_classes.models import TaggedModel
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class TaggedModelPd(TypedPandasDataFrame[TaggedModel]):
    model: type[TaggedModel] = TaggedModel
    id: str = 'id'
    price: str = 'price'
    country: str = 'country'
    name: str = 'name'

    @property
    def id_col(self) -> pd.Series:
        return self._df[self.id]

    @property
    def price_col(self) -> pd.Series:
        return self._df[self.price]

    @property
    def country_col(self) -> pd.Series:
        return self._df[self.country]

    @property
    def name_col(self) -> pd.Series:
        return self._df[self.name]

    @classmethod
    def columns_with_tag(cls, tag: Literal['map_key', 'unit_price', 'total_price', 'country']) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
