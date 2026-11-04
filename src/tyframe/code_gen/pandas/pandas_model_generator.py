"""Generator for creating BaseDfModel from pandas DataFrames."""

from typing import cast, override

import numpy as np
import pandas as pd

from tyframe.code_gen.dtype_mapping import PandasDtypeMapping
from tyframe.code_gen.pydantic_model_generator import (
    PydanticModelGenerator,
    PydanticModelGeneratorConfig,
)


class PandasModelGenerator(PydanticModelGenerator[pd.DataFrame, PandasDtypeMapping]):
    """Generator for creating BaseDfModel from pandas DataFrames."""

    def __init__(
        self,
        config: PydanticModelGeneratorConfig,
        dtype_mapping: PandasDtypeMapping | None = None,
        generated_class_suffix: str = 'PdModel',
    ) -> None:
        """Initialize the generator.

        Args:
            config: The generator configuration.
            dtype_mapping: Optional dtype mapping. If None, uses PandasDtypeMapping.
            generated_class_suffix: Suffix to append to generated class names.

        """
        super().__init__(
            config,
            dtype_mapping=dtype_mapping or PandasDtypeMapping(),
            generated_class_suffix=generated_class_suffix,
        )

    @override
    def _extract_columns_and_types(self, df: pd.DataFrame) -> dict[str, str]:
        """Extract column names and Pydantic types from a pandas DataFrame.

        Args:
            df: A pandas DataFrame.

        Returns:
            dict[str, str]: A dictionary mapping column names to Pydantic type annotations.

        """

        columns_and_types: dict[str, str] = {}

        for col_name in df.columns:
            dtype = df[col_name].dtype
            py_type = self._dtype_mapping.get_pydantic_type(cast(np.dtype, dtype))
            columns_and_types[col_name] = py_type

        return columns_and_types

    @override
    def _get_df_name(self, df: pd.DataFrame) -> str | None:
        """Get a suggested class name from the pandas DataFrame.

        Args:
            df: A pandas DataFrame.

        Returns:
            str | None: A suggested class name, or None if not available.

        """
        return None
