"""Tests for DtypeMapping classes."""

import numpy as np
import polars as pl
import pytest

from tyframe.code_gen.dtype_mapping import PandasDtypeMapping, PolarsDtypeMapping
from tyframe.exceptions.base_exception import TyframeError


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

    def test_get_pydantic_type_int(self) -> None:
        """Test getting Pydantic type for integer dtype."""

        mapping = PandasDtypeMapping()
        result = mapping.get_pydantic_type(np.dtype('int64'))

        assert result == 'int'

    def test_get_pydantic_type_float(self) -> None:
        """Test getting Pydantic type for float dtype."""

        mapping = PandasDtypeMapping()
        result = mapping.get_pydantic_type(np.dtype('float64'))

        assert result == 'float'

    def test_get_pydantic_type_bool(self) -> None:
        """Test getting Pydantic type for bool dtype."""

        mapping = PandasDtypeMapping()
        result = mapping.get_pydantic_type(np.dtype('bool'))

        assert result == 'bool'

    def test_get_pydantic_type_object(self) -> None:
        """Test getting Pydantic type for object dtype."""

        mapping = PandasDtypeMapping()
        result = mapping.get_pydantic_type(np.dtype('object'))

        assert result == 'str'

    def test_get_pydantic_type_missing_key(self) -> None:
        """Test that accessing a missing dtype raises TyframeError."""

        mapping = PandasDtypeMapping()

        with pytest.raises(TyframeError) as exc_info:
            mapping.get_pydantic_type(np.dtype('complex128'))

        assert 'not found in mapping' in str(exc_info.value)

    def test_get_dtypes(self) -> None:
        """Test getting dtypes for a Python type."""

        mapping = PandasDtypeMapping()
        result = mapping.get_dtypes(int)

        # All integer dtypes should be returned
        assert np.dtype('int8') in result
        assert np.dtype('int16') in result
        assert np.dtype('int32') in result
        assert np.dtype('int64') in result
        assert np.dtype('uint8') in result

    def test_get_dtypes_missing_key(self) -> None:
        """Test that accessing a missing Python type raises TyframeError."""
        mapping = PandasDtypeMapping()

        with pytest.raises(TyframeError) as exc_info:
            mapping.get_dtypes(complex)

        assert 'not found in mapping' in str(exc_info.value)

    def test_custom_mapping(self) -> None:
        """Test that custom mapping can be provided."""
        from collections.abc import Mapping


        custom_mapping: Mapping[np.dtype, type] = {
            np.dtype('int64'): int,
            np.dtype('float64'): float,
        }

        mapping = PandasDtypeMapping(custom_mapping)

        assert mapping.get_pydantic_type(np.dtype('int64')) == 'int'
        assert mapping.get_pydantic_type(np.dtype('float64')) == 'float'

        # The custom mapping only has these two entries
        with pytest.raises(TyframeError):
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
        """Test that accessing a missing dtype raises TyframeError."""
        from collections.abc import Mapping


        # Test with a limited custom mapping
        custom_mapping: Mapping[type[pl.DataType], type] = {pl.Int64: int}
        limited_mapping = PolarsDtypeMapping(custom_mapping)

        with pytest.raises(TyframeError) as exc_info:
            limited_mapping.get_pydantic_type(pl.Float64)

        assert 'not found in mapping' in str(exc_info.value)

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
        """Test that accessing a missing Python type raises TyframeError."""
        mapping = PolarsDtypeMapping()

        with pytest.raises(TyframeError) as exc_info:
            mapping.get_dtypes(complex)

        assert 'not found in mapping' in str(exc_info.value)

    def test_custom_mapping(self) -> None:
        """Test that custom mapping can be provided."""
        from collections.abc import Mapping


        custom_mapping: Mapping[type[pl.DataType], type] = {
            pl.Int64: int,
            pl.Float64: float,
        }

        mapping = PolarsDtypeMapping(custom_mapping)

        assert mapping.get_pydantic_type(pl.Int64) == 'int'
        assert mapping.get_pydantic_type(pl.Float64) == 'float'

        # The custom mapping only has these two entries
        with pytest.raises(TyframeError):
            mapping.get_pydantic_type(pl.Boolean)
