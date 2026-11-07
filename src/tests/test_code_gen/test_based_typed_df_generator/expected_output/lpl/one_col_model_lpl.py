import polars as pl
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OneColModel
from tyframe.typed_df.polars.typed_lazy_polars import TypedLazyPolarsDataFrame

class OneColModelLpl(TypedLazyPolarsDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = "a"

    @property
    def a_col(self) -> pl.Series:
        return self._df.select(self.a).collect().to_series()
