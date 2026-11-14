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

    def _find_code_gen_section(
        self,
        content: str,
    ) -> tuple[str, str, str] | None:
        """Find and extract the code-gen section from existing file content.

        Returns:
            A tuple of (before_start, code_gen_section, after_end) if both markers are found,
            otherwise None.
        """
        start_marker = self.config.code_gen_start
        end_marker = self.config.code_gen_end

        start_idx = content.find(start_marker)
        if start_idx == -1:
            return None

        content_after_start = content[start_idx:]
        end_idx = content_after_start.find(end_marker)
        if end_idx == -1:
            return None

        end_idx_in_full = start_idx + end_idx
        before_start = content[:start_idx]
        after_end = content[end_idx_in_full + len(end_marker) :]
        code_gen_section = content[start_idx : end_idx_in_full + len(end_marker)]

        return (before_start, code_gen_section, after_end)

    def generate_code_gen_section(
        self,
        model: type[BaseDfModel],
    ) -> str:
        """Generate only the content between code-gen markers (including markers)."""
        return '\n'.join(
            [
                self.config.code_gen_start,
                *self.generate_class(model),
                self.config.code_gen_end,
            ]
        )

    def generate_typed_df_file(
        self,
        model: type[BaseDfModel],
        output_path: Path,
    ) -> Path:
        file = output_path / f'{to_snake(self.class_name(model))}.py'
        file.parent.mkdir(exist_ok=True, parents=True)

        if file.exists():
            existing_content = file.read_text()
            section_parts = self._find_code_gen_section(existing_content)

            if section_parts is not None:
                before_start, _, after_end = section_parts
                new_code_gen_section = self.generate_code_gen_section(model)

                with file.open('w') as f:
                    f.write(before_start)
                    f.write(new_code_gen_section)
                    f.write(after_end)
                return file

        # File doesn't exist or markers not found, write full content
        with file.open('w') as f:
            _ = f.write(self.generate_typed_df_class(model))

        return file

    def _generate_init_file(
        self,
        output_path: Path,
        generated_data: list[tuple[Path, str]],
    ) -> Path:
        """Generate or update the __init__.py file to import all generated typed df classes.

        Args:
            output_path: The output directory path.
            generated_data: List of tuples containing (file_path, class_name).

        Returns:
            Path to the generated/updated __init__.py file.
        """
        init_file = output_path / '__init__.py'

        # Collect all generated files from the output directory
        # Include both newly generated files and existing ones
        all_files_data: list[tuple[Path, str]] = []

        # First, add all existing generated files (excluding __init__.py)
        if output_path.exists():
            for existing_file in output_path.glob('*.py'):
                if existing_file.name == '__init__.py':
                    continue
                # Extract class name from file content
                class_name = self._extract_class_name_from_file(existing_file)
                if class_name:
                    all_files_data.append((existing_file, class_name))

        # Then, add/update with the newly generated files
        # Use a dict to avoid duplicates, keyed by file path
        file_dict = {f[0].name: (f[0], f[1]) for f in all_files_data}
        for file_path, class_name in generated_data:
            file_dict[file_path.name] = (file_path, class_name)

        # Convert back to list and sort by class name
        sorted_data = sorted(file_dict.values(), key=lambda x: x[1])

        # Generate import statements
        import_lines: list[str] = []
        class_names: list[str] = []
        for file_path, class_name in sorted_data:
            module_name = file_path.stem
            import_lines.append(f'from .{module_name} import {class_name}')
            class_names.append(class_name)

        # Handle __all__ export
        all_export = f'__all__ = [{", ".join(f'"{name}"' for name in class_names)}]'

        # Combine all lines
        init_content = '\n'.join([*import_lines, '', all_export, ''])

        # Write the file
        init_file.parent.mkdir(exist_ok=True, parents=True)
        with init_file.open('w') as f:
            f.write(init_content)

        return init_file

    def _extract_class_name_from_file(self, file_path: Path) -> str | None:
        """Extract the class name from a generated file.

        Args:
            file_path: Path to the generated file.

        Returns:
            The class name if found, otherwise None.
        """
        if not file_path.exists():
            return None

        content = file_path.read_text()
        start_marker = self.config.code_gen_start
        end_marker = self.config.code_gen_end

        # Find the code-gen section
        start_idx = content.find(start_marker)
        if start_idx == -1:
            return None

        content_after_start = content[start_idx:]
        end_idx = content_after_start.find(end_marker)
        if end_idx == -1:
            return None

        # Extract the section between markers
        code_gen_section = content[start_idx : start_idx + end_idx]

        # Find the class definition line (first line after start marker that starts with 'class')
        for line in code_gen_section.split('\n'):
            stripped_line = line.strip()
            if stripped_line.startswith('class '):
                # Extract class name
                return stripped_line.split(' ')[1].split('(')[0].split(':')[0]

        return None

    def generate_for_input_file(
        self,
        input_file: Path,
        output_path: Path,
    ) -> list[tuple[Path, str]]:
        """Generate typed df files for models in a single input file.

        Args:
            input_file: Path to the input Python file.
            output_path: Path to the output directory.

        Returns:
            List of tuples containing (generated_file_path, class_name).
        """
        models = find_child_classes(input_file, BaseDfModel)
        return [(self.generate_typed_df_file(model, output_path), self.class_name(model)) for model in models]

    def _generate_from_single_file(
        self,
        input_file: Path,
        output_path: Path,
    ) -> list[Path]:
        """Generate typed df files from a single input file and update __init__.py.
        
        Args:
            input_file: Path to a single input Python file.
            output_path: Path to the output directory.
            
        Returns:
            List of Path objects for the generated files.
        """
        files_and_classes = self.generate_for_input_file(input_file, output_path)
        if files_and_classes:
            _ = self._generate_init_file(output_path, files_and_classes)
        return [f[0] for f in files_and_classes]

    def _generate_from_directory(
        self,
        input_dir: Path,
        output_path: Path,
    ) -> list[Path]:
        """Generate typed df files from all files in a directory and update __init__.py.
        
        Args:
            input_dir: Path to the input directory.
            output_path: Path to the output directory.
            
        Returns:
            List of Path objects for the generated files.
        """
        all_generated: list[tuple[Path, str]] = []
        for file in input_dir.glob('*.py'):
            if file.name == '__init__.py':
                continue
            all_generated.extend(self.generate_for_input_file(file, output_path))

        if all_generated:
            _ = self._generate_init_file(output_path, all_generated)

        return [f[0] for f in all_generated]

    def generate_for_input_path(
        self,
        input_path: Path,
        output_path: Path,
    ) -> list[Path]:
        if input_path.is_file():
            return self._generate_from_single_file(input_path, output_path)
        return self._generate_from_directory(input_path, output_path)

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
