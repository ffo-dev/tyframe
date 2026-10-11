from pathlib import Path

from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import (
    LazyPolarsTypedDfGenerator,
    PolarsTypedDfGenerator,
)

if __name__ == '__main__':
    output_path = Path(__file__).parent
    input_path = Path('src/tyframe/dummy')
    pl_generator = PolarsTypedDfGenerator(TypedDfGeneratorConfig())
    _ = pl_generator.generate_for_input_path(input_path, output_path / 'polars')
    lazy_pl_generator = LazyPolarsTypedDfGenerator(TypedDfGeneratorConfig())
    _ = lazy_pl_generator.generate_for_input_path(
        input_path, output_path / 'lazy_polars'
    )
    pandas_generator = PandasTypedDfGenerator(TypedDfGeneratorConfig())
    _ = pandas_generator.generate_for_input_path(input_path, output_path / 'pandas')
