from pathlib import Path

from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import (
    LazyPolarsTypedDfGenerator,
    PolarsTypedDfGenerator,
)
from tyframe.dummy.test_model import ExampleModel

if __name__ == "__main__":
    pl_generator = PolarsTypedDfGenerator(TypedDfGeneratorConfig())
    generated_code = pl_generator.generate_typed_df_class(ExampleModel)
    print(generated_code)
    with open(Path(__file__).parent / "generated_typed_polars_df.py", "w") as f:
        _ = f.write(generated_code)
    lazy_pl_generator = LazyPolarsTypedDfGenerator(TypedDfGeneratorConfig())
    lazy_generated_code = lazy_pl_generator.generate_typed_df_class(ExampleModel)
    print(lazy_generated_code)
    with open(Path(__file__).parent / "generated_typed_lazy_polars_df.py", "w") as f:
        _ = f.write(lazy_generated_code)

    pandas_generator = PandasTypedDfGenerator(TypedDfGeneratorConfig())
    pandas_code = pandas_generator.generate_typed_df_class(ExampleModel)
    with open(Path(__file__).parent / "generated_typed_pandas_df.py", "w") as f:
        _ = f.write(pandas_code)
