import polars as pl
from benchmark.source_classes.models import C10
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class C10Pl(TypedPolarsDataFrame[C10]):
    model: type[C10] = C10
    c_1: str = 'c_1'
    c_2: str = 'c_2'
    c_3: str = 'c_3'
    c_4: str = 'c_4'
    c_5: str = 'c_5'
    c_6: str = 'c_6'
    c_7: str = 'c_7'
    c_8: str = 'c_8'
    c_9: str = 'c_9'
    c_10: str = 'c_10'

    @property
    def c_1_col(self) -> pl.Series:
        return self._df[self.c_1]

    @property
    def c_2_col(self) -> pl.Series:
        return self._df[self.c_2]

    @property
    def c_3_col(self) -> pl.Series:
        return self._df[self.c_3]

    @property
    def c_4_col(self) -> pl.Series:
        return self._df[self.c_4]

    @property
    def c_5_col(self) -> pl.Series:
        return self._df[self.c_5]

    @property
    def c_6_col(self) -> pl.Series:
        return self._df[self.c_6]

    @property
    def c_7_col(self) -> pl.Series:
        return self._df[self.c_7]

    @property
    def c_8_col(self) -> pl.Series:
        return self._df[self.c_8]

    @property
    def c_9_col(self) -> pl.Series:
        return self._df[self.c_9]

    @property
    def c_10_col(self) -> pl.Series:
        return self._df[self.c_10]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
