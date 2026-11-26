import pandas as pd
from tests.test_classes.models import OneColModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class OneColModelPd(TypedPandasDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = 'a'

    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
