import pandas as pd
from benchmark.source_classes.models import PkCheck
from tyframe.tagging import TyframeTag
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class PkCheckPd(TypedPandasDataFrame[PkCheck]):
    model: type[PkCheck] = PkCheck
    id: str = 'id'

    @property
    def id_col(self) -> pd.Series:
        return self._df[self.id]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
