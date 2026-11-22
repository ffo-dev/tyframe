from pathlib import Path
from typing import Annotated

import typer

from tyframe.cli.cli_app import app
from tyframe.code_gen.based_typed_df_generator import TypedDfGeneratorConfig
from tyframe.code_gen.implemented_generators import IMPLEMENTED_GENERATORS
from tyframe.constants import IMPLEMENTED_DF_TYPES

DEFAULT_CONFIG_PATH = Path('tyframe_config.yaml')


@app.command()
def generate_typed_wrapper(
    *,
    input_path: Annotated[
        Path,
        typer.Option(
            '--input-path',
            help='Python file or directory containing the BaseDfModel subclasses to generate wrappers for.',
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Option(
            '--output-path',
            help='Directory where the generated typed DataFrame wrapper files are written.',
            file_okay=False,
            dir_okay=True,
        ),
    ],
    config_path: Annotated[
        Path,
        typer.Option(
            '--config-path',
            help='Generator configuration file (YAML or JSON), e.g. indentation size and column property suffix.',
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ] = DEFAULT_CONFIG_PATH,
    df_type: Annotated[
        IMPLEMENTED_DF_TYPES,
        typer.Option('--df-type', help='DataFrame library to generate the wrapper for.'),
    ],
    class_suffix: Annotated[
        str,
        typer.Option(
            '--class-suffix',
            help='Suffix appended to each model name to build the generated class name, e.g. "Pl" -> TransactionPl.',
        ),
    ],
) -> None:
    """Generate typed DataFrame wrappers for every BaseDfModel subclass found under --input-path.

    Example:

        tyframe generate-typed-wrapper --input-path src/in --output-path src/out --df-type polars --class-suffix Pl
    """
    generator_ctor = IMPLEMENTED_GENERATORS[df_type]
    generator = generator_ctor(
        TypedDfGeneratorConfig.from_file(config_path),
        class_suffix,
    )
    _ = generator.generate_for_input_path(
        input_path,
        output_path,
    )
