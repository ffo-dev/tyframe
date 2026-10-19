from pathlib import Path

import pytest

from tyframe.code_gen.based_typed_df_generator import BasedTypedDfGenerator, TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import LazyPolarsTypedDfGenerator, PolarsTypedDfGenerator


# Parametrize the generators to test all implementations
@pytest.mark.parametrize(
    ('generator_type', 'expected_suffix'),
    [
        (PandasTypedDfGenerator, 'pd'),
        (PolarsTypedDfGenerator, 'pl'),
        (LazyPolarsTypedDfGenerator, 'lpl'),
    ],
)
def test_generate_for_input_path_with_single_file(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
    expected_suffix: str,
) -> None:
    """Test generate_for_input_path with a single input file for all generators."""
    # Use the existing test_classes.models file
    from tests.test_classes import models
    input_file = Path(models.__file__)

    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that we got at least one file (there are multiple models in the file)
    assert len(result_files) > 0

    # Check that all files have the correct suffix
    for file in result_files:
        assert file.name.endswith(f'_{expected_suffix}.py')
        assert file.parent == output_path

        # Read and verify the generated content
        generated_content = file.read_text()
        assert 'class' in generated_content


@pytest.mark.parametrize(
    ('generator_type', 'expected_suffix'),
    [
        (PandasTypedDfGenerator, 'pd'),
        (PolarsTypedDfGenerator, 'pl'),
        (LazyPolarsTypedDfGenerator, 'lpl'),
    ],
)
def test_generate_for_input_path_with_directory(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
    expected_suffix: str,
) -> None:
    """Test generate_for_input_path with a directory containing multiple files for all generators."""
    # Use the test_classes directory which has multiple model files
    from tests.test_classes import models
    input_dir = Path(models.__file__).parent

    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_dir, output_path)

    # Check that we got files for the models (not __init__.py)
    assert len(result_files) >= 1

    # Check that all files have the correct suffix
    for file in result_files:
        assert file.name.endswith(f'_{expected_suffix}.py')
        assert file.parent == output_path


@pytest.mark.parametrize(
    ('generator_type'),
    [
        (PandasTypedDfGenerator),
        (PolarsTypedDfGenerator),
        (LazyPolarsTypedDfGenerator),
    ],
)
def test_generate_for_input_path_with_empty_directory(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
) -> None:
    """Test generate_for_input_path with an empty directory for all generators."""
    input_dir = tmp_path / 'empty_dir'
    input_dir.mkdir()

    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_dir, output_path)

    # Check that we got no files
    assert len(result_files) == 0


@pytest.mark.parametrize(
    ('generator_type', 'expected_suffix'),
    [
        (PandasTypedDfGenerator, 'pd'),
        (PolarsTypedDfGenerator, 'pl'),
        (LazyPolarsTypedDfGenerator, 'lpl'),
    ],
)
def test_generate_for_input_path_creates_output_directory(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
    expected_suffix: str,
) -> None:
    """Test that generate_for_input_path creates the output directory if it doesn't exist for all generators."""
    # Use the existing test_classes.models file
    from tests.test_classes import models
    input_file = Path(models.__file__)

    # Use a non-existent output directory
    output_path = tmp_path / 'new_output' / 'nested'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that the output directory was created
    assert output_path.exists()
    assert len(result_files) > 0
    assert all(file.parent == output_path for file in result_files)


@pytest.mark.parametrize(
    ('generator_type', 'expected_suffix'),
    [
        (PandasTypedDfGenerator, 'pd'),
        (PolarsTypedDfGenerator, 'pl'),
        (LazyPolarsTypedDfGenerator, 'lpl'),
    ],
)
def test_generate_for_input_path_with_config_from_file(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
    expected_suffix: str,
) -> None:
    """Test generate_for_input_path with configuration loaded from file for all generators."""
    # Create a config file
    config_file = tmp_path / 'config.yml'
    config_file.write_text("""col_property_suffix: '_col'
indentation_size: 2
""")

    # Create a generator with config from file
    config = TypedDfGeneratorConfig.from_file(config_file)
    generator = generator_type(config=config)

    # Use the existing test_classes.models file
    from tests.test_classes import models
    input_file = Path(models.__file__)

    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that we got at least one file
    assert len(result_files) > 0

    # Check that the indentation in the generated file is 2 spaces
    generated_content = result_files[0].read_text()
    # The indentation should be 2 spaces in the generated class
    assert '  model:' in generated_content or '  a:' in generated_content
