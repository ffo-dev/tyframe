"""Tests for BasedTypedDfGenerator generate_for_input_path functionality."""

from pathlib import Path

import pytest

from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OneColModel
from tyframe.code_gen.based_typed_df_generator import BasedTypedDfGenerator, TypedDfGeneratorConfig
from tyframe.code_gen.pandas import PandasTypedDfGenerator
from tyframe.code_gen.polars import LazyPolarsTypedDfGenerator, PolarsTypedDfGenerator


def _compare_with_expected(
    generated: str,
    expected_path: Path,
) -> None:
    """Compare generated code with expected file, ignoring empty lines.

    Args:
        generated: The generated code string.
        expected_path: Path to the expected output file.

    Raises:
        AssertionError: If the generated and expected content don't match.
    """
    expected = expected_path.read_text()

    # Strip and split by lines, filtering out empty lines
    generated_lines = [line for line in generated.strip().split('\n') if line.strip()]
    expected_lines = [line for line in expected.strip().split('\n') if line.strip()]

    # Compare line by line
    assert generated_lines == expected_lines, (
        f'Generated code does not match expected.\nGenerated:\n{generated}\nExpected:\n{expected}'
    )


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
    # Use the local input_class.example_models file
    input_file = Path(__file__).parent / 'input_class' / 'example_models.py'
    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that we got files for all models (OneColModel, TwoColModel, OtherExample)
    assert len(result_files) == 3

    # Check that all files have the correct suffix
    expected_filenames = [
        f'one_col_model_{expected_suffix}.py',
        f'two_col_model_{expected_suffix}.py',
        f'other_example_{expected_suffix}.py',
    ]
    actual_filenames = sorted([file.name for file in result_files])
    assert sorted(expected_filenames) == actual_filenames

    # Check that all files are in the output directory
    for file in result_files:
        assert file.parent == output_path

    # Compare each generated file with its expected version
    for result_file in result_files:
        expected_file = Path(__file__).parent / 'expected_output' / expected_suffix / result_file.name
        assert expected_file.exists(), f'Expected file {expected_file} does not exist'
        generated_content = result_file.read_text()
        _compare_with_expected(generated_content, expected_file)


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
    # Use the input_class directory which contains example_models.py
    input_dir = Path(__file__).parent / 'input_class'
    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_dir, output_path)

    # Check that we got files for the models (not __init__.py)
    assert len(result_files) == 3

    # Check that all files have the correct suffix
    expected_filenames = [
        f'one_col_model_{expected_suffix}.py',
        f'two_col_model_{expected_suffix}.py',
        f'other_example_{expected_suffix}.py',
    ]
    actual_filenames = sorted([file.name for file in result_files])
    assert sorted(expected_filenames) == actual_filenames

    # Check that all files are in the output directory
    for file in result_files:
        assert file.parent == output_path

    # Compare each generated file with its expected version
    for result_file in result_files:
        expected_file = Path(__file__).parent / 'expected_output' / expected_suffix / result_file.name
        assert expected_file.exists(), f'Expected file {expected_file} does not exist'
        generated_content = result_file.read_text()
        _compare_with_expected(generated_content, expected_file)


@pytest.mark.parametrize(
    'generator_type',
    [
        PandasTypedDfGenerator,
        PolarsTypedDfGenerator,
        LazyPolarsTypedDfGenerator,
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
    # Use the local input_class.example_models file
    input_file = Path(__file__).parent / 'input_class' / 'example_models.py'

    # Use a non-existent output directory
    output_path = tmp_path / 'new_output' / 'nested'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that the output directory was created
    assert output_path.exists()
    assert len(result_files) == 3
    assert all(file.parent == output_path for file in result_files)

    # Compare each generated file with its expected version
    for result_file in result_files:
        expected_file = Path(__file__).parent / 'expected_output' / expected_suffix / result_file.name
        assert expected_file.exists(), f'Expected file {expected_file} does not exist'
        generated_content = result_file.read_text()
        _compare_with_expected(generated_content, expected_file)


@pytest.mark.parametrize(
    'generator_type',
    [
        PandasTypedDfGenerator,
        PolarsTypedDfGenerator,
        LazyPolarsTypedDfGenerator,
    ],
)
def test_generate_for_input_path_with_config_from_file(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
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

    # Use the local input_class.example_models file
    input_file = Path(__file__).parent / 'input_class' / 'example_models.py'
    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that we got files
    assert len(result_files) == 3

    # Check that the indentation in the generated files is 2 spaces
    for file in result_files:
        generated_content = file.read_text()
        # The indentation should be 2 spaces in the generated class
        assert '  model:' in generated_content or '  a:' in generated_content

    # Also check that the col_property_suffix is correctly applied
    for file in result_files:
        generated_content = file.read_text()
        assert '_col' in generated_content


@pytest.mark.parametrize(
    'generator_type',
    [
        PandasTypedDfGenerator,
        PolarsTypedDfGenerator,
        LazyPolarsTypedDfGenerator,
    ],
)
def test_generate_typed_df_file_idempotent(
    tmp_path: Path,
    generator_type: type[BasedTypedDfGenerator],
) -> None:
    """Test that generate_typed_df_file is idempotent - running it twice produces the same result."""
    # Use the local input_class.example_models file
    input_file = Path(__file__).parent / 'input_class' / 'example_models.py'
    output_path = tmp_path / 'output'
    generator = generator_type(config=TypedDfGeneratorConfig())

    # Generate the typed df files the first time
    result_files = generator.generate_for_input_path(input_file, output_path)
    assert len(result_files) == 3

    # Read the content of all generated files
    first_contents = {file.name: file.read_text() for file in result_files}

    # Generate again - should update in place
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Read the content again
    second_contents = {file.name: file.read_text() for file in result_files}

    # Content should be identical
    assert first_contents == second_contents


def test_generate_typed_df_file_preserves_existing_content_polars(
    tmp_path: Path,
) -> None:
    """Test that generate_typed_df_file preserves content outside code-gen markers for Polars."""

    generator = PolarsTypedDfGenerator(config=TypedDfGeneratorConfig())
    output_path = tmp_path / 'output'
    output_path.mkdir(parents=True)

    # Create a file with existing content before and after markers
    existing_file = output_path / 'one_col_model_pl.py'
    existing_content = '''import polars as pl
from tests.test_code_gen.test_based_typed_df_generator.input_class.example_models import OneColModel
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame

# This is a comment that should be preserved

#### CODE-GEN START
class OneColModelPl(TypedPolarsDataFrame[OneColModel]):
    model: type[OneColModel] = OneColModel
    a: str = "a"
    @property
    def a_col(self) -> pl.Series:
        return self._df[self.a]
#### CODE-GEN END

    def custom_method(self) -> str:
        """This is a custom method that should be preserved."""
        return "custom"
'''
    existing_file.write_text(existing_content)

    # Generate the file
    result = generator.generate_typed_df_file(OneColModel, output_path)

    # Read the generated content
    generated_content = result.read_text()

    # Check that the comment before the markers is preserved
    assert '# This is a comment that should be preserved' in generated_content

    # Check that the custom method after the markers is preserved
    assert 'def custom_method(self) -> str:' in generated_content
    assert 'This is a custom method that should be preserved' in generated_content
