import pandas as pd
from tests.test_classes.models import CustomTagModel, MyTag
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame


#### CODE-GEN START
class CustomTagModelPd(TypedPandasDataFrame[CustomTagModel]):
    model: type[CustomTagModel] = CustomTagModel
    a: str = 'a'
    b: str = 'b'
    c: str = 'c'

    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]

    @property
    def b_col(self) -> pd.Series:
        return self._df[self.b]

    @property
    def c_col(self) -> pd.Series:
        return self._df[self.c]

    @classmethod
    def columns_with_tag(cls, tag: MyTag) -> list[str]:
        return cls.model.columns_with_tag(tag)


#### CODE-GEN END
