import polars as pl
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import TwoColModel
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame
#### CODE-GEN START
class TwoColModelPl(TypedPolarsDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel
    a: str = "a"
    b: str = "b"
    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]
    @property
    def b_col(self) -> pl.Series:
        return self._df[self.b]
#### CODE-GEN END