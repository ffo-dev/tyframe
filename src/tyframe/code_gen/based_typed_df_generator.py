from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

from tyframe.base_df_model.base_df_model import BaseDfModel


class TypedDfGeneratorConfig(BaseModel):
    """
    Configuration for the TypedDfGenerator.
    """

    col_property_suffix: str = "_col"
    indentation_size: int = 4


class BasedTypedDfGenerator(metaclass=ABCMeta):
    config: TypedDfGeneratorConfig
    _indentation: str
    _generated_class_suffix: str

    def __init__(
        self, config: TypedDfGeneratorConfig, generated_class_suffix: str = "TypedDf"
    ):
        self.config = config
        self._indentation = " " * self.config.indentation_size
        self._generated_class_suffix = generated_class_suffix

    def generate_typed_df_class(
        self,
        model: type[BaseDfModel],
    ) -> str:
        """
        Generate a typed DataFrame class based on the provided Pydantic model.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the python code for the generated typed DataFrame class.
        """
        return "\n".join(self._raw_generate_typed_df_class(model))

    def _raw_generate_typed_df_class(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """
        Generate the lines of code for the typed DataFrame class based on the provided Pydantic model.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.
        Returns:
            list[str]: A list of strings representing the lines of code for the generated typed DataFrame class.
        """
        return [
            *self._generate_imports(model),
            *self._generate_class(model),
        ]

    def _generate_imports(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """
        Generate the import statements required for the typed DataFrame class.

        Returns:
            list[str]: A list of strings representing the import statements.
        """
        return [
            self._df_library_import(),
            *self._additional_imports(),
            self._model_import(model),
            self._typed_df_base_class_import(),
        ]

    def _additional_imports(self) -> list[str]:
        """
        Generate any additional import statements required for the typed DataFrame class.

        Returns:
            list[str]: A list of strings representing the additional import statements.
        """
        return []

    @abstractmethod
    def _df_library_import(self) -> str:
        """
        Generate the import statement for the DataFrame library (e.g., pandas, polars).

        Returns:
            str: A string representing the import statement for the DataFrame library.
        """
        raise NotImplementedError  # pragma: no cover

    def _model_import(self, model: type[BaseDfModel]) -> str:
        """
        Generate the import statement for the Pydantic model.

        Args:
            model: The Pydantic model class to generate the import statement for.
        """
        return f"from {model.__module__} import {model.__name__}"

    @abstractmethod
    def _typed_df_base_class_import(self) -> str:
        """
        Generate the import statement for the base typed DataFrame class.

        Returns:
            str: A string representing the import statement for the base typed DataFrame class.
        """
        raise NotImplementedError  # pragma: no cover

    def _generate_class(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """
        Generate the class definition for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the class definition.
        """
        return [
            self._generate_class_definition(model),
            self._generate_model_type_variable(model),
            *self._generate_class_variables(model),
            *self._generate_columns_properties(model),
        ]

    @abstractmethod
    def _typed_df_name(self) -> str:
        """
        Get the name of the base typed DataFrame class.

        Returns:
            str: A string representing the name of the base typed DataFrame class.
        """
        raise NotImplementedError  # pragma: no cover

    def _generate_class_definition(
        self,
        model: type[BaseDfModel],
    ) -> str:
        return f"class {model.__name__}{self._generated_class_suffix}({self._typed_df_name()}[{model.__name__}]):"

    def _generate_model_type_variable(self, model: type[BaseDfModel]) -> str:
        """
        Generate the model type variable for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            str: A string representing the model type variable.
        """
        return f"{self._indentation}model: type[{model.__name__}] = {model.__name__}"

    def _generate_class_variable(
        self,
        col_name: str,
    ) -> str:
        """
        Generate a class variable for the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the class variable for.

        Returns:
            str: A string representing the class variable.
        """
        return f'{self._indentation}{col_name}: str = "{col_name}"'

    def _generate_class_variables(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """
        Generate the class variables for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            list[str]: A list of strings representing the class variables.
        """
        return [self._generate_class_variable(col_name) for col_name in model.columns]

    @abstractmethod
    def _col_return_type(self) -> str:
        """
        Get the DataFrame library type (e.g., pandas.DataFrame, polars.DataFrame).

        Returns:
            str: A string representing the DataFrame library type.
        """
        raise NotImplementedError  # pragma: no cover

    def _get_df_column(
        self,
        col_name: str,
    ) -> str:
        """
        Generate a property for a column in the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the property for.

        Returns:
            str: A string representing the property.
        """
        return f"return self._df[self.{col_name}]"

    def _generate_column_property(
        self,
        col_name: str,
    ) -> list[str]:
        """
        Generate a property for a column in the typed DataFrame class.

        Args:
            col_name: The name of the column to generate the property for.

        Returns:
            list[str]: A list of strings representing the property.
        """
        return [
            f"{self._indentation}@property",
            f"{self._indentation}def {col_name}{self.config.col_property_suffix}(self) -> {self._col_return_type()}:",
            f"{self._indentation * 2}{self._get_df_column(col_name)}",
        ]

    def _generate_columns_properties(
        self,
        model: type[BaseDfModel],
    ) -> list[str]:
        """
        Generate the column properties for the typed DataFrame class.

        Args:
            model: The Pydantic model class to generate the typed DataFrame class for.

        Returns:
            list[str]: A list of strings representing the column properties.
        """
        return [
            line
            for col_name in model.columns
            for line in self._generate_column_property(col_name)
        ]
