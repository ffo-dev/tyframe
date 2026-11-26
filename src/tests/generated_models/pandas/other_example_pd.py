import pandas as pd
from tests.test_classes.models import OtherExample
from tyframe.tagging import TyframeTag
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class OtherExamplePd(TypedPandasDataFrame[OtherExample]):
    model: type[OtherExample] = OtherExample
    yaba: str = 'yaba'

    @property
    def yaba_col(self) -> pd.Series:
        return self._df[self.yaba]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
