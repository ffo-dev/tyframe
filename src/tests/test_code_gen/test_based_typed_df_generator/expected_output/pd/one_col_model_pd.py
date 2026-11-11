import pandas as pd
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OneColModel
from tyframe.typed_df.pandas.typed_pandas import TypedPandasDataFrame
#### CODE-GEN START
class OneColModelPd(TypedPandasDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = "a"
    @property
    def a_col(self) -> pd.Series:
        return self._df[self.a]
#### CODE-GEN END