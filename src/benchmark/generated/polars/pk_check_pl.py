import polars as pl
from benchmark.source_classes.models import PkCheck
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class PkCheckPl(TypedPolarsDataFrame[PkCheck]):
    model: type[PkCheck] = PkCheck
    id: str = 'id'

    @property
    def id_col(self) -> pl.Series:
        return self._df[self.id]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
