"""Dtype mapping classes for converting dataframe types to Pydantic types."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta
from typing import TypeVar

import numpy as np
import polars as pl

from tyframe.exceptions.base_exception import TyframeError

# Type variable for the dataframe dtype
DataFrameDtype = TypeVar('DataFrameDtype')


class DtypeMapping[DataFrameDtype](metaclass=ABCMeta):
    """Abstract base class for dtype mappings.
    
    This is a generic class that should be parameterized with the specific dtype type
    for the dataframe library (e.g., pandas dtype or polars DataType).
    """

    _df_type_to_py_type: Mapping[DataFrameDtype, type]
    _py_types_to_df_types: Mapping[type, Sequence[DataFrameDtype]]
    _available_py_types: set[type]
    _available_df_types: set[DataFrameDtype]

    def __init__(self, mapping: Mapping[DataFrameDtype, type] | None = None):
        if mapping is None:
            self._df_type_to_py_type = self.default()
        else:
            self._df_type_to_py_type = mapping
        # Build reverse mapping: Python type -> list of dataframe dtypes
        self._py_types_to_df_types = self._build_reverse_mapping(self._df_type_to_py_type)
        self._available_py_types = set(self._py_types_to_df_types.keys())
        self._available_df_types = set(self._df_type_to_py_type.keys())

    @staticmethod
    def _build_reverse_mapping(mapping: Mapping[DataFrameDtype, type]) -> Mapping[type, Sequence[DataFrameDtype]]:
        """Build a reverse mapping from Python types to dataframe dtypes."""
        reverse: dict[type, list[DataFrameDtype]] = {}
        for df_dtype, py_type in mapping.items():
            if py_type not in reverse:
                reverse[py_type] = []
            reverse[py_type].append(df_dtype)
        return reverse

    def get_pydantic_type(self, dtype: DataFrameDtype) -> str:
        """Get the Pydantic type for a given dataframe dtype.

        Args:
            dtype: The dataframe dtype to map.

        Returns:
            str: The corresponding Pydantic type as a string.

        Raises:
            TyframeError: If the dtype is not found in the mapping.

        """
        if dtype not in self._df_type_to_py_type:
            raise TyframeError(f'Dtype {dtype} not found in mapping')
        return self._df_type_to_py_type[dtype].__name__

    def get_dtypes(self, type_: type) -> Sequence[DataFrameDtype]:
        """Get all dtype keys that map to the given Python type.

        Args:
            type_: The Python type to filter by.

        Returns:
            Sequence[DataFrameDtype]: Sequence of dtype keys that map to the given type.

        Raises:
            TyframeError: If the Python type is not found in the mapping.

        """
        if type_ not in self._py_types_to_df_types:
            raise TyframeError(f'Python type {type_} not found in mapping')
        return self._py_types_to_df_types[type_]

    @abstractmethod
    def default(self) -> Mapping[DataFrameDtype, type]:
        raise NotImplementedError


class PandasDtypeMapping(DtypeMapping['np.dtype']):
    """Dtype mapping for pandas DataFrames.
    
    Uses actual numpy dtype objects as keys in the mapping.
    """

    def default(self) -> Mapping[np.dtype, type]:
        return {
            np.dtype('int8'): int,
            np.dtype('int16'): int,
            np.dtype('int32'): int,
            np.dtype('int64'): int,
            np.dtype('uint8'): int,
            np.dtype('uint16'): int,
            np.dtype('uint32'): int,
            np.dtype('uint64'): int,
            np.dtype('float16'): float,
            np.dtype('float32'): float,
            np.dtype('float64'): float,
            np.dtype('bool'): bool,
            np.dtype('object'): str,
            np.dtype('datetime64[ns]'): datetime,
            np.dtype('timedelta64[ns]'): timedelta,
        }

class PolarsDtypeMapping(DtypeMapping['type[pl.DataType]']):
    """Dtype mapping for polars DataFrames.
    
    Uses actual polars DataType classes as keys in the mapping.
    """

    def default(self) -> Mapping[type[pl.DataType], type]:
        return {
            pl.Int8: int,
            pl.Int16: int,
            pl.Int32: int,
            pl.Int64: int,
            pl.UInt8: int,
            pl.UInt16: int,
            pl.UInt32: int,
            pl.UInt64: int,
            pl.Float32: float,
            pl.Float64: float,
            pl.Boolean: bool,
            pl.String: str,
            pl.Utf8: str,
            pl.Date: date,
            pl.Datetime: datetime,
            pl.Time: timedelta,
            pl.Duration: timedelta,
            pl.Categorical: str,
        }
