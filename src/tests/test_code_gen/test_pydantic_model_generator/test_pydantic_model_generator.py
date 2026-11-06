"""Tests for PydanticModelGenerator."""

from pathlib import Path

import pandas as pd
import polars as pl
import pytest

from tyframe.code_gen.pandas.pandas_model_generator import PandasModelGenerator
from tyframe.code_gen.polars.polars_model_generator import PolarsModelGenerator
from tyframe.code_gen.pydantic_model_generator import PydanticModelGeneratorConfig


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


# Test DataFrames
SIMPLE_PANDAS_DF = pd.DataFrame(
    {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
    }
)

SIMPLE_POLARS_DF = pl.DataFrame(
    {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
    }
)

COMPLEX_PANDAS_DF = pd.DataFrame(
    {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000.0, 60000.0, 70000.0],
        'is_active': [True, False, True],
    }
)

COMPLEX_POLARS_DF = pl.DataFrame(
    {
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000.0, 60000.0, 70000.0],
        'is_active': [True, False, True],
    }
)


@pytest.mark.parametrize(
    ('generator_class', 'df', 'expected_file'),
    [
        (PandasModelGenerator, SIMPLE_PANDAS_DF, 'simple_model.py'),
        (PolarsModelGenerator, SIMPLE_POLARS_DF, 'simple_model.py'),
    ],
)
def test_generate_simple_model(
    tmp_path: Path,
    generator_class: type[PandasModelGenerator | PolarsModelGenerator],
    df: pd.DataFrame | pl.DataFrame,
    expected_file: str,
) -> None:
    """Test generating a simple model from DataFrame."""
    # Create generator and generate model
    config = PydanticModelGeneratorConfig()
    generator = generator_class(config)
    generated = generator.generate_model_class(df, 'SimpleModel')  # pyright: ignore[reportArgumentType]

    # Compare with expected
    expected_path = Path(__file__).parent / 'expected' / expected_file
    _compare_with_expected(generated, expected_path)


@pytest.mark.parametrize(
    ('generator_class', 'df', 'expected_file'),
    [
        (PandasModelGenerator, COMPLEX_PANDAS_DF, 'complex_model.py'),
        (PolarsModelGenerator, COMPLEX_POLARS_DF, 'complex_model.py'),
    ],
)
def test_generate_complex_model(
    tmp_path: Path,
    generator_class: type[PandasModelGenerator | PolarsModelGenerator],
    df: pd.DataFrame | pl.DataFrame,
    expected_file: str,
) -> None:
    """Test generating a complex model with multiple types."""
    # Create generator and generate model
    config = PydanticModelGeneratorConfig()
    generator = generator_class(config)
    generated = generator.generate_model_class(df, 'ComplexModel')  # pyright: ignore[reportArgumentType]

    # Compare with expected
    expected_path = Path(__file__).parent / 'expected' / expected_file
    _compare_with_expected(generated, expected_path)


@pytest.mark.parametrize(
    ('generator_class', 'df'),
    [
        (PandasModelGenerator, SIMPLE_PANDAS_DF),
        (PolarsModelGenerator, SIMPLE_POLARS_DF),
    ],
)
def test_generate_with_custom_indentation(
    tmp_path: Path,
    generator_class: type[PandasModelGenerator | PolarsModelGenerator],
    df: pd.DataFrame | pl.DataFrame,
) -> None:
    """Test generating with custom indentation size."""
    # Create generator with custom indentation
    config = PydanticModelGeneratorConfig(indentation_size=2)
    generator = generator_class(config)
    generated = generator.generate_model_class(df, 'SimpleModel')  # pyright: ignore[reportArgumentType]

    # Check that indentation is 2 spaces
    assert '  id: int' in generated
    assert '  name: str' in generated
    assert '  age: int' in generated


@pytest.mark.parametrize(
    ('generator_class', 'df', 'expected_file'),
    [
        (PandasModelGenerator, SIMPLE_PANDAS_DF, 'simple_model.py'),
        (PolarsModelGenerator, SIMPLE_POLARS_DF, 'simple_model.py'),
    ],
)
def test_generate_model_file(
    tmp_path: Path,
    generator_class: type[PandasModelGenerator | PolarsModelGenerator],
    df: pd.DataFrame | pl.DataFrame,
    expected_file: str,
) -> None:
    """Test generating and saving a model to a file."""
    # Create generator and generate file
    config = PydanticModelGeneratorConfig()
    generator = generator_class(config)
    output_path = tmp_path / 'output'

    file_path = generator.generate_model_file(df, output_path, 'SimpleModel')  # pyright: ignore[reportArgumentType]

    # Check that file was created
    assert file_path.exists()
    assert file_path.parent == output_path

    # Check file content
    expected_path = Path(__file__).parent / 'expected' / expected_file
    _compare_with_expected(file_path.read_text(), expected_path)


@pytest.mark.parametrize(
    ('generator_class', 'df', 'expected_suffix'),
    [
        (PandasModelGenerator, SIMPLE_PANDAS_DF, 'Model'),
        (PolarsModelGenerator, SIMPLE_POLARS_DF, 'Model'),
    ],
)
def test_generate_without_class_name(
    generator_class: type[PandasModelGenerator | PolarsModelGenerator],
    df: pd.DataFrame | pl.DataFrame,
    expected_suffix: str,
) -> None:
    """Test generating a model without specifying a class name."""
    # Create generator and generate model without class name
    config = PydanticModelGeneratorConfig()
    generator = generator_class(config)
    generated = generator.generate_model_class(df, None)  # pyright: ignore[reportArgumentType]

    # Check that default class name is used
    assert f'DataFrame{expected_suffix}' in generated
