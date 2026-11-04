"""Dtype mapping classes for converting dataframe types to Pydantic types."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta
from typing import TypeVar

import numpy as np
import polars as pl

# Type variable for the dataframe dtype
DataFrameDtype = TypeVar('DataFrameDtype')


class DtypeMapping[DataFrameDtype](metaclass=ABCMeta):
    """Abstract base class for dtype mappings.
    
    This is a generic class that should be parameterized with the specific dtype type
    for the dataframe library (e.g., pandas dtype or polars DataType).
    """

    _df_type_to_py_type: Mapping[DataFrameDtype, type]
    _py_types_to_df_types: Mapping[type, Sequence[DataFrameDtype]]

    def __init__(self, mapping: Mapping[DataFrameDtype, type] | None = None):
        if mapping is None:
            self._df_type_to_py_type = self.default()
        else:
            self._df_type_to_py_type = mapping

    def get_pydantic_type(self, dtype: DataFrameDtype) -> str:
        """Get the Pydantic type for a given dataframe dtype.

        Args:
            dtype: The dataframe dtype to map.

        Returns:
            str: The corresponding Pydantic type as a string.

        """
        return self._df_type_to_py_type[dtype].__name__

    def get_dtypes(self, type_: type) -> list[DataFrameDtype]:
        """Get all dtype keys that map to the given Python type.

        Args:
            type_: The Python type to filter by.

        Returns:
            list[DataFrameDtype]: List of dtype keys that map to the given type.

        """
        return [k for k, v in self._df_type_to_py_type.items() if v is type_]

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
