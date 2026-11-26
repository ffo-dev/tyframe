from typing import Literal

import polars as pl
from tests.test_classes.models import CustomTagModel
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class CustomTagModelPl(TypedPolarsDataFrame[CustomTagModel]):
    model: type[CustomTagModel] = CustomTagModel
    a: str = 'a'
    b: str = 'b'
    c: str = 'c'

    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]

    @property
    def b_col(self) -> pl.Series:
        return self._df[self.b]

    @property
    def c_col(self) -> pl.Series:
        return self._df[self.c]

    @classmethod
    def columns_with_tag(cls, tag: Literal['custom', 'map_key']) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
