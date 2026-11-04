from typing import override

import pandas as pd

from tyframe.code_gen.pydantic_model_generator import (
    PydanticModelGenerator,
    PydanticModelGeneratorConfig,
)


class PandasModelGenerator(PydanticModelGenerator[pd.DataFrame]):
    """Generator for creating BaseDfModel from pandas DataFrames."""

    def __init__(
        self,
        config: PydanticModelGeneratorConfig,
        generated_class_suffix: str = 'PdModel',
    ) -> None:
        super().__init__(config, generated_class_suffix)

    @override
    def _extract_columns_and_types(self, df: pd.DataFrame) -> dict[str, str]:
        """Extract column names and Pydantic types from a pandas DataFrame.

        Args:
            df: A pandas DataFrame.

        Returns:
            dict[str, str]: A dictionary mapping column names to Pydantic type annotations.

        """

        type_mapping = self._get_pandas_type_mapping()
        columns_and_types: dict[str, str] = {}

        for col_name in df.columns:
            dtype = df[col_name].dtype
            py_type = type_mapping.get(str(dtype), 'Any')
            columns_and_types[col_name] = py_type

        return columns_and_types

    def _get_pandas_type_mapping(self) -> dict[str, str]:
        """Get the mapping from pandas dtypes to Pydantic types.

        Returns:
            dict[str, str]: A dictionary mapping pandas dtype strings to Pydantic type strings.

        """
        return {
            'int8': 'int',
            'int16': 'int',
            'int32': 'int',
            'int64': 'int',
            'uint8': 'int',
            'uint16': 'int',
            'uint32': 'int',
            'uint64': 'int',
            'float16': 'float',
            'float32': 'float',
            'float64': 'float',
            'bool': 'bool',
            'object': 'str',
            'string': 'str',
            'datetime64[ns]': 'datetime',
            'timedelta64[ns]': 'timedelta',
            'category': 'str',
        }

    @override
    def _get_df_name(self, df: pd.DataFrame) -> str | None:
        """Get a suggested class name from the pandas DataFrame.

        Args:
            df: A pandas DataFrame.

        Returns:
            str | None: A suggested class name, or None if not available.

        """
        return None
