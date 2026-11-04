"""Abstract base class for generating BaseDfModel from dataframes."""

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Any, TypeVar

from pydantic.alias_generators import to_snake

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.config import BaseCodeGeneratorConfig
from tyframe.code_gen.dtype_mapping import DtypeMapping

DataFrameType = TypeVar('DataFrameType')
DtypeMappingType = TypeVar('DtypeMappingType', bound=DtypeMapping[Any])


class PydanticModelGeneratorConfig(BaseCodeGeneratorConfig):
    """Configuration for the PydanticModelGenerator."""

    pass


class PydanticModelGenerator[DataFrameType, DtypeMappingType](metaclass=ABCMeta):
    """Abstract base class for generating BaseDfModel from dataframes."""

    config: PydanticModelGeneratorConfig
    _dtype_mapping: DtypeMappingType
    _generated_class_suffix: str

    def __init__(
        self,
        config: PydanticModelGeneratorConfig,
        dtype_mapping: DtypeMappingType,
        generated_class_suffix: str = 'Model',
    ) -> None:
        """Initialize the generator.

        Args:
            config: The generator configuration.
            dtype_mapping: The dtype mapping instance for converting dataframe types to Pydantic types.
            generated_class_suffix: Suffix to append to generated class names.

        """
        self.config = config
        self._dtype_mapping = dtype_mapping
        self._generated_class_suffix = generated_class_suffix

    def generate_model_class(
        self,
        df: DataFrameType,
        class_name: str | None = None,
    ) -> str:
        """Generate a BaseDfModel class from a dataframe.

        Args:
            df: The dataframe to generate the model from.
            class_name: Optional name for the generated class. If None, will use dataframe name or 'DataFrameModel'.

        Returns:
            str: A string representing the python code for the generated BaseDfModel class.

        """
        return '\n'.join(self._raw_generate_model_class(df, class_name))

    def generate_model_file(
        self,
        df: DataFrameType,
        output_path: Path,
        class_name: str | None = None,
    ) -> Path:
        """Generate a BaseDfModel class from a dataframe and save it to a file.

        Args:
            df: The dataframe to generate the model from.
            output_path: The directory to save the generated file.
            class_name: Optional name for the generated class.

        Returns:
            Path: The path to the generated file.

        """
        actual_class_name = class_name or self._get_df_name(df) or 'DataFrame'
        file_name = f'{to_snake(actual_class_name)}{self._generated_class_suffix}.py'
        file = output_path / file_name
        file.parent.mkdir(exist_ok=True, parents=True)
        with file.open('w') as f:
            _ = f.write(self.generate_model_class(df, class_name))
        return file

    def _raw_generate_model_class(
        self,
        df: DataFrameType,
        class_name: str | None,
    ) -> list[str]:
        """Generate the lines of code for the BaseDfModel class.

        Args:
            df: The dataframe to generate the model from.
            class_name: Optional name for the generated class.

        Returns:
            list[str]: A list of strings representing the lines of code.

        """
        actual_class_name = class_name or self._get_df_name(df) or 'DataFrame'
        model_name = f'{actual_class_name}{self._generated_class_suffix}'
        
        return [
            self._generate_imports(),
            '',
            self._generate_class_definition(model_name),
            *self._generate_field_definitions(df),
        ]

    def _generate_imports(self) -> str:
        """Generate the import statement for BaseDfModel.

        Returns:
            str: The import statement.

        """
        return f'from {BaseDfModel.__module__} import {BaseDfModel.__name__}'

    def _generate_class_definition(self, class_name: str) -> str:
        """Generate the class definition line.

        Args:
            class_name: The name of the generated class.

        Returns:
            str: The class definition line.

        """
        return f'class {class_name}({BaseDfModel.__name__}):'

    def _generate_field_definitions(self, df: DataFrameType) -> list[str]:
        """Generate the field definitions for the model.

        Args:
            df: The dataframe to generate fields from.

        Returns:
            list[str]: A list of field definition lines.

        """
        columns_and_types = self._extract_columns_and_types(df)
        return [
            f'{self.config.indentation}{col_name}: {py_type}'
            for col_name, py_type in columns_and_types.items()
        ]

    @abstractmethod
    def _extract_columns_and_types(self, df: DataFrameType) -> dict[str, str]:
        """Extract column names and their corresponding Pydantic types from the dataframe.

        Args:
            df: The dataframe to extract types from.

        Returns:
            dict[str, str]: A dictionary mapping column names to Pydantic type annotations.

        """
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def _get_df_name(self, df: DataFrameType) -> str | None:
        """Get a suggested class name from the dataframe.

        Args:
            df: The dataframe to get the name from.

        Returns:
            str | None: A suggested class name, or None if not available.

        """
        raise NotImplementedError  # pragma: no cover
