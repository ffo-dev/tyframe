"""Tests for DtypeMapping classes."""

from collections.abc import Mapping

import numpy as np
import polars as pl
import pytest

from tyframe.validation.dtype_mapping import (
    DtypeNotFoundError,
    PandasDtypeMapping,
    PolarsDtypeMapping,
    PyTypeNotFoundError,
)


class TestPandasDtypeMapping:
    """Tests for PandasDtypeMapping."""

    def test_default_mapping_initialized(self) -> None:
        """Test that default mapping is initialized correctly."""

        mapping = PandasDtypeMapping()

        # Check that the mapping works correctly
        assert mapping.get_pydantic_type(np.dtype('int64')) == 'int'
        assert mapping.get_pydantic_type(np.dtype('float64')) == 'float'
        assert mapping.get_pydantic_type(np.dtype('bool')) == 'bool'
        assert mapping.get_pydantic_type(np.dtype('object')) == 'str'

    def test_get_pydantic_type_missing_key(self) -> None:
        """Test that accessing a missing dtype raises DtypeNotFoundError."""

        mapping = PandasDtypeMapping()

        with pytest.raises(DtypeNotFoundError) as exc_info:
            mapping.get_pydantic_type(np.dtype('complex128'))

        assert 'not found in mapping' in str(exc_info.value)
        assert 'Available dtypes' in str(exc_info.value)

    def test_get_dtypes(self) -> None:
        """Test getting dtypes for a Python type."""

        mapping = PandasDtypeMapping()
        result = mapping.get_dtypes(int)

        # All integer dtypes should be returned
        assert sorted(result) == sorted(
            [np.dtype('int8'), np.dtype('int16'), np.dtype('int32'), np.dtype('int64'), np.dtype('uint8')],
        )

    def test_get_dtypes_missing_key(self) -> None:
        """Test that accessing a missing Python type raises PyTypeNotFoundError."""
        mapping = PandasDtypeMapping()

        with pytest.raises(PyTypeNotFoundError) as exc_info:
            mapping.get_dtypes(complex)

        assert 'not found in mapping' in str(exc_info.value)
        assert 'Available Python types' in str(exc_info.value)

    def test_custom_mapping(self) -> None:
        """Test that custom mapping can be provided."""

        custom_mapping: Mapping[np.dtype, type] = {
            np.dtype('int64'): int,
            np.dtype('float64'): float,
        }

        mapping = PandasDtypeMapping(custom_mapping)

        assert mapping.get_pydantic_type(np.dtype('int64')) == 'int'
        assert mapping.get_pydantic_type(np.dtype('float64')) == 'float'

        # The custom mapping only has these two entries
        with pytest.raises(DtypeNotFoundError):
            mapping.get_pydantic_type(np.dtype('bool'))


class TestPolarsDtypeMapping:
    """Tests for PolarsDtypeMapping."""

    def test_default_mapping_initialized(self) -> None:
        """Test that default mapping is initialized correctly."""

        mapping = PolarsDtypeMapping()

        # Check that the mapping works correctly
        assert mapping.get_pydantic_type(pl.Int64) == 'int'
        assert mapping.get_pydantic_type(pl.Float64) == 'float'
        assert mapping.get_pydantic_type(pl.Boolean) == 'bool'
        assert mapping.get_pydantic_type(pl.String) == 'str'

    def test_get_pydantic_type_int(self) -> None:
        """Test getting Pydantic type for integer dtype."""

        mapping = PolarsDtypeMapping()
        result = mapping.get_pydantic_type(pl.Int64)

        assert result == 'int'

    def test_get_pydantic_type_float(self) -> None:
        """Test getting Pydantic type for float dtype."""

        mapping = PolarsDtypeMapping()
        result = mapping.get_pydantic_type(pl.Float64)

        assert result == 'float'

    def test_get_pydantic_type_bool(self) -> None:
        """Test getting Pydantic type for bool dtype."""

        mapping = PolarsDtypeMapping()
        result = mapping.get_pydantic_type(pl.Boolean)

        assert result == 'bool'

    def test_get_pydantic_type_string(self) -> None:
        """Test getting Pydantic type for string dtype."""

        mapping = PolarsDtypeMapping()
        result = mapping.get_pydantic_type(pl.String)

        assert result == 'str'

    def test_get_pydantic_type_missing_key(self) -> None:
        """Test that accessing a missing dtype raises DtypeNotFoundError."""

        # Test with a limited custom mapping
        custom_mapping: Mapping[type[pl.DataType], type] = {pl.Int64: int}
        limited_mapping = PolarsDtypeMapping(custom_mapping)

        with pytest.raises(DtypeNotFoundError) as exc_info:
            limited_mapping.get_pydantic_type(pl.Float64)

        assert 'not found in mapping' in str(exc_info.value)
        assert 'Available dtypes' in str(exc_info.value)

    def test_get_dtypes(self) -> None:
        """Test getting dtypes for a Python type."""

        mapping = PolarsDtypeMapping()
        result = mapping.get_dtypes(int)

        # All integer dtypes should be returned
        assert pl.Int8 in result
        assert pl.Int16 in result
        assert pl.Int32 in result
        assert pl.Int64 in result
        assert pl.UInt8 in result

    def test_get_dtypes_missing_key(self) -> None:
        """Test that accessing a missing Python type raises PyTypeNotFoundError."""
        mapping = PolarsDtypeMapping()

        with pytest.raises(PyTypeNotFoundError) as exc_info:
            mapping.get_dtypes(complex)

        assert 'not found in mapping' in str(exc_info.value)
        assert 'Available Python types' in str(exc_info.value)

    def test_custom_mapping(self) -> None:
        """Test that custom mapping can be provided."""

        custom_mapping: Mapping[type[pl.DataType], type] = {
            pl.Int64: int,
            pl.Float64: float,
        }

        mapping = PolarsDtypeMapping(custom_mapping)

        assert mapping.get_pydantic_type(pl.Int64) == 'int'
        assert mapping.get_pydantic_type(pl.Float64) == 'float'

        # The custom mapping only has these two entries
        with pytest.raises(DtypeNotFoundError):
            mapping.get_pydantic_type(pl.Boolean)
