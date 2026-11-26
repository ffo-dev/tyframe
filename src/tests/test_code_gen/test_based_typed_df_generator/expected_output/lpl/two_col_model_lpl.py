import polars as pl
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import TwoColModel
from tyframe.tagging import TyframeTag
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame
#### CODE-GEN START
class TwoColModelLpl(TypedLazyPolarsDataFrame[TwoColModel]):
    model: type[TwoColModel] = TwoColModel
    a: str = "a"
    b: str = "b"
    @property
    def a_col(self) -> pl.Series:
        return self._df.select(self.a).collect().to_series()
    @property
    def b_col(self) -> pl.Series:
        return self._df.select(self.b).collect().to_series()
    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        return cls.model.columns_with_tag(tag)
#### CODE-GEN END