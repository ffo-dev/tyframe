"""Generator for creating BaseDfModel from polars DataFrames."""

from typing import override

import polars as pl

from tyframe.code_gen.dtype_mapping import DtypeMapping, PolarsDtypeMapping
from tyframe.code_gen.pydantic_model_generator import (
    PydanticModelGenerator,
    PydanticModelGeneratorConfig,
)


class PolarsModelGenerator(PydanticModelGenerator[pl.DataFrame, PolarsDtypeMapping]):
    """Generator for creating BaseDfModel from polars DataFrames."""

    def __init__(
        self,
        config: PydanticModelGeneratorConfig,
        dtype_mapping: PolarsDtypeMapping | None = None,
        generated_class_suffix: str = 'PlModel',
    ) -> None:
        """Initialize the generator.

        Args:
            config: The generator configuration.
            dtype_mapping: Optional dtype mapping. If None, uses PolarsDtypeMapping.
            generated_class_suffix: Suffix to append to generated class names.

        """
        super().__init__(
            config,
            dtype_mapping=dtype_mapping or PolarsDtypeMapping(),
            generated_class_suffix=generated_class_suffix,
        )

    @override
    def _extract_columns_and_types(self, df: pl.DataFrame) -> dict[str, str]:
        """Extract column names and Pydantic types from a polars DataFrame.

        Args:
            df: A polars DataFrame.

        Returns:
            dict[str, str]: A dictionary mapping column names to Pydantic type annotations.

        """

        columns_and_types: dict[str, str] = {}

        for col_name, dtype in df.schema.items():
            py_type = self._dtype_mapping.get_pydantic_type(dtype)
            columns_and_types[col_name] = py_type

        return columns_and_types

    @override
    def _get_df_name(self, df: pl.DataFrame) -> str | None:
        """Get a suggested class name from the polars DataFrame.

        Args:
            df: A polars DataFrame.

        Returns:
            str | None: A suggested class name, or None if not available.

        """
        return None
