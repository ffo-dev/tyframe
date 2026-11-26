import pandas as pd
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import TwoColModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame
#### CODE-GEN START
class TwoColModelPd(TypedPandasDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel
    a: str = "a"
    b: str = "b"
    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]
    @property
    def b_col(self) -> pd.Series:
        return self._df[self.b]
    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)
#### CODE-GEN END