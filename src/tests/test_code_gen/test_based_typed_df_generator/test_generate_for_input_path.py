from pathlib import Path
from typing import override

import pytest

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.based_typed_df_generator import (
    BasedTypedDfGenerator,
    TypedDfGeneratorConfig,
)


# Create a test implementation of BasedTypedDfGenerator for testing
class TestTypedDfGenerator(BasedTypedDfGenerator):
    """Test implementation of BasedTypedDfGenerator for unit tests."""

    @override
    def _df_library_import(self) -> str:
        return 'import test_df as td'

    @override
    def _typed_df_base_class_import(self) -> str:
        return 'from test_module import TestTypedDf'

    @override
    def _typed_df_name(self) -> str:
        return 'TestTypedDf'

    @override
    def _col_return_type(self) -> str:
        return 'td.Series'


# Create test models in a temporary module
class TestModelA(BaseDfModel):
    col_a: int
    col_b: str


class TestModelB(BaseDfModel):
    x: float
    y: int


class TestModelC(BaseDfModel):
    name: str


# Fixture for generator
@pytest.fixture
def generator() -> TestTypedDfGenerator:
    config = TypedDfGeneratorConfig()
    return TestTypedDfGenerator(config, generated_class_suffix='Test')


# Fixture for config
@pytest.fixture
def config() -> TypedDfGeneratorConfig:
    return TypedDfGeneratorConfig()


def test_generate_for_input_path_with_single_file(tmp_path: Path, generator: TestTypedDfGenerator) -> None:
    """Test generate_for_input_path with a single input file."""
    # Create a temporary input file with a test model
    input_file = tmp_path / 'test_models.py'
    input_file.write_text(
        """from tyframe.base_df_model.base_df_model import BaseDfModel

class SingleModel(BaseDfModel):
    field_a: int
    field_b: str
"""
    )

    # Add the tmp_path to sys.path so the file can be imported
    import sys
    sys.path.insert(0, str(tmp_path))

    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that we got the expected file
    assert len(result_files) == 1
    assert result_files[0].name == 'single_model_test.py'
    assert result_files[0].parent == output_path

    # Read and verify the generated content
    generated_content = result_files[0].read_text()
    assert 'class SingleModelTest' in generated_content
    assert 'TestTypedDf[SingleModel]' in generated_content
    assert 'field_a' in generated_content
    assert 'field_b' in generated_content

    # Clean up sys.path
    sys.path.remove(str(tmp_path))


def test_generate_for_input_path_with_directory(tmp_path: Path, generator: TestTypedDfGenerator) -> None:
    """Test generate_for_input_path with a directory containing multiple files."""
    # Create a temporary directory with multiple model files
    input_dir = tmp_path / 'input_models'
    input_dir.mkdir()

    # Create first model file
    (input_dir / 'models_a.py').write_text(
        """from tyframe.base_df_model.base_df_model import BaseDfModel

class ModelA(BaseDfModel):
    col_a: int
"""
    )

    # Create second model file
    (input_dir / 'models_b.py').write_text(
        """from tyframe.base_df_model.base_df_model import BaseDfModel

class ModelB(BaseDfModel):
    col_b: str
    col_c: float
"""
    )

    # Create __init__.py which should be ignored
    (input_dir / '__init__.py').write_text('')

    # Create a non-py file which should be ignored
    (input_dir / 'readme.txt').write_text('This should be ignored')

    # Add the tmp_path to sys.path so the files can be imported
    import sys
    sys.path.insert(0, str(tmp_path))

    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_dir, output_path)

    # Check that we got files for both model files (not __init__.py)
    assert len(result_files) == 2
    file_names = sorted([f.name for f in result_files])
    assert file_names == ['models_a.py', 'models_b.py']

    # Check that the output directory contains the expected files
    output_files = sorted(output_path.glob('*.py'))
    assert len(output_files) == 2
    assert Path('model_a_test.py') in [f.relative_to(output_path) for f in output_files]
    assert Path('model_b_test.py') in [f.relative_to(output_path) for f in output_files]

    # Clean up sys.path
    sys.path.remove(str(tmp_path))


def test_generate_for_input_path_with_empty_directory(tmp_path: Path, generator: TestTypedDfGenerator) -> None:
    """Test generate_for_input_path with an empty directory."""
    input_dir = tmp_path / 'empty_dir'
    input_dir.mkdir()

    # Add the tmp_path to sys.path
    import sys
    sys.path.insert(0, str(tmp_path))

    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_dir, output_path)

    # Check that we got no files
    assert len(result_files) == 0

    # Clean up sys.path
    sys.path.remove(str(tmp_path))


def test_generate_for_input_path_creates_output_directory(tmp_path: Path, generator: TestTypedDfGenerator) -> None:
    """Test that generate_for_input_path creates the output directory if it doesn't exist."""
    # Create a temporary input file
    input_file = tmp_path / 'test_model.py'
    input_file.write_text(
        """from tyframe.base_df_model.base_df_model import BaseDfModel

class TestModel(BaseDfModel):
    value: int
"""
    )

    # Add the tmp_path to sys.path
    import sys
    sys.path.insert(0, str(tmp_path))

    # Use a non-existent output directory
    output_path = tmp_path / 'new_output' / 'nested'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that the output directory was created
    assert output_path.exists()
    assert len(result_files) == 1
    assert result_files[0].parent == output_path

    # Clean up sys.path
    sys.path.remove(str(tmp_path))


def test_generate_for_input_path_with_config_from_file(tmp_path: Path) -> None:
    """Test generate_for_input_path with configuration loaded from file."""
    # Create a config file
    config_file = tmp_path / 'config.yml'
    config_file.write_text("""col_property_suffix: '_col'
indentation_size: 2
""")

    # Create a test generator with config from file
    config = TypedDfGeneratorConfig.from_file(config_file)
    generator = TestTypedDfGenerator(config, generated_class_suffix='Test')

    # Create a temporary input file
    input_file = tmp_path / 'test_model.py'
    input_file.write_text(
        """from tyframe.base_df_model.base_df_model import BaseDfModel

class TestModel(BaseDfModel):
    value: int
"""
    )

    # Add the tmp_path to sys.path
    import sys
    sys.path.insert(0, str(tmp_path))

    output_path = tmp_path / 'output'

    # Generate the typed df files
    result_files = generator.generate_for_input_path(input_file, output_path)

    # Check that the indentation in the generated file is 2 spaces
    generated_content = result_files[0].read_text()
    # The indentation should be 2 spaces in the generated class
    assert '  model:' in generated_content or '  value:' in generated_content

    # Clean up sys.path
    sys.path.remove(str(tmp_path))
