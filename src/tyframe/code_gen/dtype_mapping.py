"""Dtype mapping classes for converting dataframe types to Pydantic types."""

from __future__ import annotations

from abc import ABCMeta
from collections.abc import Mapping
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

    _mapping: Mapping[DataFrameDtype, type]

    def get_pydantic_type(self, dtype: DataFrameDtype) -> str:
        """Get the Pydantic type for a given dataframe dtype.

        Args:
            dtype: The dataframe dtype to map.

        Returns:
            str: The corresponding Pydantic type as a string.

        """
        return self._mapping[dtype].__name__

    def get_dtypes(self, type_: type) -> list[DataFrameDtype]:
        """Get all dtype keys that map to the given Python type.

        Args:
            type_: The Python type to filter by.

        Returns:
            list[DataFrameDtype]: List of dtype keys that map to the given type.

        """
        return [k for k, v in self._mapping.items() if v is type_]


class PandasDtypeMapping(DtypeMapping['np.dtype']):
    """Dtype mapping for pandas DataFrames.
    
    Uses actual numpy dtype objects as keys in the mapping.
    """

    def __init__(self) -> None:
        """Initialize the pandas dtype mapping with actual numpy dtype objects as keys."""

        self._mapping = {
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

    def __init__(self) -> None:
        """Initialize the polars dtype mapping with DataType objects as keys."""
        import polars as pl

        self._mapping = {
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

    def get_dtypes(self, type_: type) -> list[type[pl.DataType]]:
        """Get all dtype keys that map to the given Python type."""
        return [k for k, v in self._mapping.items() if v is type_]
