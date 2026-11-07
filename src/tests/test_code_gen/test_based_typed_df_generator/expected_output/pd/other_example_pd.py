import pandas as pd
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OtherExample
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame

class OtherExamplePd(TypedPandasDataFrame[OtherExample]):
    model: type[OtherExample] = OtherExample
    yaba: str = "yaba"

    @property
    def yaba_col(self) -> pd.Series:
        return self._df[self.yaba]
