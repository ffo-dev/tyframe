from abc import ABCMeta, abstractmethod
from pathlib import Path

from pydantic.alias_generators import to_snake

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.class_finder import find_child_classes
from tyframe.code_gen.config import BaseCodeGeneratorConfig


class TypedDfGeneratorConfig(BaseCodeGeneratorConfig):
    """Configuration for the TypedDfGenerator."""

    col_property_suffix: str = '_col'


class BasedTypedDfGenerator(metaclass=ABCMeta):
    config: TypedDfGeneratorConfig
    _generated_class_suffix: str

    def __init__(
        self,
        config: TypedDfGeneratorConfig,
        generated_class_suffix: str = 'TypedDf',
    ) -> None:
        self.config = config
        self._generated_class_suffix = generated_class_suffix

    def generate_typed_df_class(
        self,
        model: type[BaseDfModel],
    ) -> str:
        """Generate a typed DataFrame class based on the provided Pydantic model.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the python code for the generated typed DataFrame class.

        """
        return '\n'.join(self.raw_generate_typed_df_class(model))

    def generate_code_gen_section(
        self,
        model: type[BaseDfModel],
    ) -> str:
        """Generate only the content between code-gen markers (including markers)."""
        return '\n'.join([
            self.config.code_gen_start,
            *self.generate_class(model),
            self.config.code_gen_end,
        ])

    def generate_typed_df_file(
        self,
        model: type[BaseDfModel],
        output_path: Path,
    ) -> Path:
        file = output_path / f'{to_snake(self.class_name(model))}.py'
        file.parent.mkdir(exist_ok=True, parents=True)

        # If file exists, update only the code-gen section; otherwise create new file
        if file.exists():
            existing_content = file.read_text()

            # Split the existing file into parts
            start_marker = self.config.code_gen_start
            end_marker = self.config.code_gen_end

            # Find the start marker
            start_idx = existing_content.find(start_marker)

            if start_idx != -1:
                # Start marker found, look for end marker
                content_after_start = existing_content[start_idx:]
                end_idx = content_after_start.find(end_marker)

                if end_idx != -1:
                    # Both markers found, construct the new file content
                    end_idx_in_full = start_idx + end_idx
                    before_start = existing_content[:start_idx]
                    after_end = existing_content[end_idx_in_full + len(end_marker):]

                    # Generate only the code-gen section (with markers)
                    new_code_gen_section = self.generate_code_gen_section(model)

                    # Write the updated file
                    with file.open('w') as f:
                        f.write(before_start)
                        f.write(new_code_gen_section)
                        f.write(after_end)
                else:
                    # Only start marker found, write the entire new content
                    with file.open('w') as f:
                        _ = f.write(self.generate_typed_df_class(model))
            else:
                # No start marker found, write the entire new content
                with file.open('w') as f:
                    _ = f.write(self.generate_typed_df_class(model))
        else:
            # File doesn't exist, create it with the full content
            with file.open('w') as f:
                _ = f.write(self.generate_typed_df_class(model))

        return file

    def generate_for_input_file(
        self,
        input_file: Path,
        output_path: Path,
    ) -> list[Path]:
        models = find_child_classes(input_file, BaseDfModel)
        return [self.generate_typed_df_file(model, output_path) for model in models]

    def generate_for_input_path(
        self,
        input_path: Path,
        output_path: Path,
    ) -> list[Path]:
        if input_path.is_file():
            return self.generate_for_input_file(input_path, output_path)
        res: list[Path] = []
        for file in input_path.glob('*.py'):
            if file.name == '__init__.py':
                continue
            res.extend(self.generate_for_input_file(file, output_path))
        return res

    def raw_generate_typed_df_class(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """Generate the lines of code for the typed DataFrame class based on the provided Pydantic model.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            list[str]: A list of strings representing the lines of code for the generated typed DataFrame class.

        """
        return [
            *self.generate_imports(model),
            *self.additional_imports(),
            self.config.code_gen_start,
            *self.generate_class(model),
            self.config.code_gen_end,
        ]

    def generate_imports(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """Generate the import statements required for the typed DataFrame class.

        Returns:
            list[str]: A list of strings representing the import statements.

        """
        return [
            self.df_library_import(),
            *self.additional_imports(),
            self.model_import(model),
            self.typed_df_base_class_import(),
        ]

    def additional_imports(self) -> list[str]:
        """Generate any additional import statements required for the typed DataFrame class.

        Returns:
            list[str]: A list of strings representing the additional import statements.

        """
        return []

    @abstractmethod
    def df_library_import(self) -> str:
        """Generate the import statement for the DataFrame library (e.g., pandas, polars).

        Returns:
            str: A string representing the import statement for the DataFrame library.

        """
        raise NotImplementedError  # pragma: no cover

    def model_import(self, model: type[BaseDfModel]) -> str:
        """Generate the import statement for the Pydantic model.

        Args:
            model: The Pydantic model class to generate the import statement for.

        """
        return f'from {model.__module__} import {model.__name__}'

    @abstractmethod
    def typed_df_base_class_import(self) -> str:
        """Generate the import statement for the base typed DataFrame class.

        Returns:
            str: A string representing the import statement for the base typed DataFrame class.

        """
        raise NotImplementedError  # pragma: no cover

    def generate_class(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """Generate the class definition for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the class definition.

        """
        return [
            self.generate_class_definition(model),
            self.generate_model_type_variable(model),
            *self.generate_class_variables(model),
            *self.generate_columns_properties(model),
        ]

    @abstractmethod
    def typed_df_name(self) -> str:
        """Get the name of the base typed DataFrame class.

        Returns:
            str: A string representing the name of the base typed DataFrame class.

        """
        raise NotImplementedError  # pragma: no cover

    def generate_class_definition(
        self,
        model: type[BaseDfModel],
    ) -> str:
        return f'class {self.class_name(model)}({self.typed_df_name()}[{model.__name__}]):'

    def class_name(self, model: type[BaseDfModel]) -> str:
        return f'{model.__name__}{self._generated_class_suffix}'

    def generate_model_type_variable(self, model: type[BaseDfModel]) -> str:
        """Generate the model type variable for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the model type variable.

        """
        return f'{self.config.indentation}model: type[{model.__name__}] = {model.__name__}'

    def generate_class_variable(
        self,
        col_name: str,
    ) -> str:
        """Generate a class variable for the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the class variable for.

        Returns:
            str: A string representing the class variable.

        """
        return f'{self.config.indentation}{col_name}: str = "{col_name}"'

    def generate_class_variables(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """Generate the class variables for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            list[str]: A list of strings representing the class variables.

        """
        return [self.generate_class_variable(col_name) for col_name in model.columns]

    @abstractmethod
    def col_return_type(self) -> str:
        """Get the DataFrame library type (e.g., pandas.DataFrame, polars.DataFrame).

        Returns:
            str: A string representing the DataFrame library type.

        """
        raise NotImplementedError  # pragma: no cover

    def get_df_column(
        self,
        col_name: str,
    ) -> str:
        """Generate a property for a column in the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the property for.

        Returns:
            str: A string representing the property.

        """
        return f'return self._df[self.{col_name}]'

    def generate_column_property(
        self,
        col_name: str,
    ) -> list[str]:
        """Generate a property for a column in the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the property for.

        Returns:
            list[str]: A list of strings representing the property.

        """
        suffix = self.config.col_property_suffix
        return [
            f'{self.config.indentation}@property',
            f'{self.config.indentation}def {col_name}{suffix}(self) -> {self.col_return_type()}:',
            f'{self.config.indentation * 2}{self.get_df_column(col_name)}',
        ]

    def generate_columns_properties(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """Generate the column properties for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            list[str]: A list of strings representing the column properties.

        """
        return [line for col_name in model.columns for line in self.generate_column_property(col_name)]
