from pathlib import Path

from tyframe.cli.cli_app import app
from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.implemented_generators import IMPLEMENTED_GENERATORS
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import (
    LazyPolarsTypedDfGenerator,
    PolarsTypedDfGenerator,
)
from tyframe.constants import IMPLEMENTED_DF_TYPES


@app.command()
def generate_typed_wrapper(
    *,
    input_path: Path,
    output_path: Path,
    config_path: Path,
    df_type: IMPLEMENTED_DF_TYPES,
    class_suffix: str,
) -> None:
    generator_ctor = IMPLEMENTED_GENERATORS[df_type]
    generator = generator_ctor(
        TypedDfGeneratorConfig.from_file(config_path),
        class_suffix,
    )
    _ = generator.generate_for_input_path(
        input_path,
        output_path,
    )

if __name__ == '__main__':
    output_path = Path(__file__).parent
    input_path = Path('src/tyframe/dummy')
    pl_generator = PolarsTypedDfGenerator(TypedDfGeneratorConfig())
    _ = pl_generator.generate_for_input_path(input_path, output_path / 'polars')
    lazy_pl_generator = LazyPolarsTypedDfGenerator(TypedDfGeneratorConfig())
    _ = lazy_pl_generator.generate_for_input_path(
        input_path, output_path / 'lazy_polars',
    )
    pandas_generator = PandasTypedDfGenerator(TypedDfGeneratorConfig())
    _ = pandas_generator.generate_for_input_path(input_path, output_path / 'pandas')
