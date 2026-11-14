import polars as pl
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OtherExample
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame
#### CODE-GEN START
class OtherExamplePl(TypedPolarsDataFrame[OtherExample]):
    model: type[OtherExample] = OtherExample
    yaba: str = "yaba"
    @property
    def yaba_col(self) -> pl.Series:
        return self._df[self.yaba]
#### CODE-GEN END