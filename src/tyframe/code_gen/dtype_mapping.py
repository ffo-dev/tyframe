"""Dtype mapping classes for converting dataframe types to Pydantic types."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    import numpy as np
    from polars.datatypes.classes import DataType

# Type variable for the dataframe dtype
DataFrameDtype = TypeVar('DataFrameDtype')


class DtypeMapping[DataFrameDtype](metaclass=ABCMeta):
    """Abstract base class for dtype mappings.
    
    This is a generic class that should be parameterized with the specific dtype type
    for the dataframe library (e.g., pandas dtype or polars DataType).
    """

    @abstractmethod
    def get_pydantic_type(self, dtype: DataFrameDtype) -> str:
        """Get the Pydantic type for a given dataframe dtype.

        Args:
            dtype: The dataframe dtype to map.

        Returns:
            str: The corresponding Pydantic type.

        """
        raise NotImplementedError


class PandasDtypeMapping(DtypeMapping["np.dtype"]):
    """Dtype mapping for pandas DataFrames.
    
    Uses actual numpy dtype objects as keys in the mapping.
    """

    def __init__(self) -> None:
        """Initialize the pandas dtype mapping with actual numpy dtype objects as keys."""
        import numpy as np

        self._mapping: dict["np.dtype", str] = {
            np.dtype('int8'): 'int',
            np.dtype('int16'): 'int',
            np.dtype('int32'): 'int',
            np.dtype('int64'): 'int',
            np.dtype('uint8'): 'int',
            np.dtype('uint16'): 'int',
            np.dtype('uint32'): 'int',
            np.dtype('uint64'): 'int',
            np.dtype('float16'): 'float',
            np.dtype('float32'): 'float',
            np.dtype('float64'): 'float',
            np.dtype('bool'): 'bool',
            np.dtype('object'): 'str',
            np.dtype('datetime64[ns]'): 'datetime',
            np.dtype('timedelta64[ns]'): 'timedelta',
        }

    def get_pydantic_type(self, dtype: "np.dtype") -> str:
        """Get the Pydantic type for a pandas dtype.

        Args:
            dtype: A numpy dtype object.

        Returns:
            str: The corresponding Pydantic type.

        """
        return self._mapping[dtype]


class PolarsDtypeMapping(DtypeMapping["DataType"]):
    """Dtype mapping for polars DataFrames.
    
    Uses actual polars DataType objects as keys in the mapping.
    """

    def __init__(self) -> None:
        """Initialize the polars dtype mapping with DataType objects as keys."""
        import polars as pl

        self._mapping: dict[type["DataType"], str] = {
            pl.Int8: 'int',
            pl.Int16: 'int',
            pl.Int32: 'int',
            pl.Int64: 'int',
            pl.UInt8: 'int',
            pl.UInt16: 'int',
            pl.UInt32: 'int',
            pl.UInt64: 'int',
            pl.Float32: 'float',
            pl.Float64: 'float',
            pl.Boolean: 'bool',
            pl.String: 'str',
            pl.Utf8: 'str',
            pl.Date: 'date',
            pl.Datetime: 'datetime',
            pl.Time: 'time',
            pl.Duration: 'timedelta',
            pl.Null: 'Any',
            pl.Categorical: 'str',
        }

    def get_pydantic_type(self, dtype: type["DataType"]) -> str:
        """Get the Pydantic type for a polars dtype.

        Args:
            dtype: A polars dtype (DataType object).

        Returns:
            str: The corresponding Pydantic type.

        """
        return self._mapping[dtype]
