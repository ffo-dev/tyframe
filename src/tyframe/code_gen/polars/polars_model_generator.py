from typing import override

import polars as pl

from tyframe.code_gen.pydantic_model_generator import (
    PydanticModelGenerator,
    PydanticModelGeneratorConfig,
)


class PolarsModelGenerator(PydanticModelGenerator[pl.DataFrame]):
    """Generator for creating BaseDfModel from polars DataFrames."""

    def __init__(
        self,
        config: PydanticModelGeneratorConfig,
        generated_class_suffix: str = 'PlModel',
    ) -> None:
        super().__init__(config, generated_class_suffix)

    @override
    def _extract_columns_and_types(self, df: pl.DataFrame) -> dict[str, str]:
        """Extract column names and Pydantic types from a polars DataFrame.

        Args:
            df: A polars DataFrame.

        Returns:
            dict[str, str]: A dictionary mapping column names to Pydantic type annotations.

        """

        type_mapping = self._get_polars_type_mapping()
        columns_and_types: dict[str, str] = {}

        for col_name, dtype in df.schema.items():
            py_type = type_mapping.get(str(dtype), 'Any')
            columns_and_types[col_name] = py_type

        return columns_and_types

    def _get_polars_type_mapping(self) -> dict[str, str]:
        """Get the mapping from polars dtypes to Pydantic types.

        Returns:
            dict[str, str]: A dictionary mapping polars dtype strings to Pydantic type strings.

        """
        return {
            'Int8': 'int',
            'Int16': 'int',
            'Int32': 'int',
            'Int64': 'int',
            'UInt8': 'int',
            'UInt16': 'int',
            'UInt32': 'int',
            'UInt64': 'int',
            'Float32': 'float',
            'Float64': 'float',
            'Boolean': 'bool',
            'String': 'str',
            'Utf8': 'str',
            'Date': 'date',
            'Datetime': 'datetime',
            'Time': 'time',
            'Duration': 'timedelta',
            'List': 'list',
            'Struct': 'dict',
            'Null': 'Any',
            'Object': 'Any',
            'Categorical': 'str',
        }

    @override
    def _get_df_name(self, df: pl.DataFrame) -> str | None:
        """Get a suggested class name from the polars DataFrame.

        Args:
            df: A polars DataFrame.

        Returns:
            str | None: A suggested class name, or None if not available.

        """
        return None
