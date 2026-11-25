"""Tests for dtype validation in BaseValidator."""

from datetime import datetime

import pandas as pd
import polars as pl
import pytest

from tyframe.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeColumnValidation
from tyframe.validation.dtype_mapping import (
    DtypeMismatchError,
)
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import LazyPolarsValidator, PolarsValidator


# Test models
class IntStrModel(BaseDfModel):
    """Model with int and str columns."""

    int_col: int
    str_col: str


class FloatModel(BaseDfModel):
    """Model with float column."""

    float_col: float


class ModelWithDefault(BaseDfModel):
    """Model with a column that has a default value."""

    int_col: int
    default_col: int = 42


class BoolModel(BaseDfModel):
    """Model with bool column."""

    bool_col: bool


class DateTimeModel(BaseDfModel):
    """Model with datetime column."""

    datetime_col: datetime


class TestDtypeValidation:
    """Test suite for dtype validation."""

    def test_pandas_validate_dtypes_success(self) -> None:
        """Test that dtype validation passes for matching types in pandas."""

        config = TyframeColumnValidation(validate_dtypes=True)
        validator = PandasValidator(config=config)
        df = pd.DataFrame(
            {
                'int_col': [1, 2, 3],
                'str_col': ['a', 'b', 'c'],
            }
        )

        result = validator.validate(IntStrModel, df)
        assert result is not None
        assert isinstance(result, pd.DataFrame)

    def test_pandas_validate_dtypes_mismatch(self) -> None:
        """Test that DtypeMismatchError is raised for mismatched types in pandas."""

        config = TyframeColumnValidation(validate_dtypes=True)
        validator = PandasValidator(config=config)
        # Create DataFrame with wrong dtype (str instead of int)
        df = pd.DataFrame(
            {
                'int_col': ['a', 'b', 'c'],  # Wrong dtype: should be int
                'str_col': ['x', 'y', 'z'],
            }
        )

        with pytest.raises(DtypeMismatchError) as exc_info:
            validator.validate(IntStrModel, df)

        error_msg = str(exc_info.value)
        assert 'int_col' in error_msg
        assert 'int' in error_msg

    def test_pandas_validate_dtypes_disabled_by_default(self) -> None:
        """Test that dtype validation is disabled by default for pandas."""

        validator = PandasValidator()
        df = pd.DataFrame(
            {
                'int_col': ['a', 'b', 'c'],  # Wrong dtype
                'str_col': ['x', 'y', 'z'],
            }
        )
        # No config specified, so validate_dtypes should be False by default
        result = validator.validate(IntStrModel, df)
        assert result is not None

    def test_polars_validate_dtypes_success(self) -> None:
        """Test that dtype validation passes for matching types in polars."""

        config = TyframeColumnValidation(validate_dtypes=True)
        validator = PolarsValidator(config=config)
        df = pl.DataFrame(
            {
                'int_col': [1, 2, 3],
                'str_col': ['a', 'b', 'c'],
            }
        )

        result = validator.validate(IntStrModel, df)
        assert result is not None
        assert isinstance(result, pl.DataFrame)

    def test_polars_validate_dtypes_mismatch(self) -> None:
        """Test that DtypeMismatchError is raised for mismatched types in polars."""

        config = TyframeColumnValidation(validate_dtypes=True)
        validator = PolarsValidator(config=config)
        # Create DataFrame with wrong dtype (str instead of int)
        df = pl.DataFrame(
            {
                'int_col': ['a', 'b', 'c'],  # Wrong dtype: should be int
                'str_col': ['x', 'y', 'z'],
            }
        )

        with pytest.raises(DtypeMismatchError) as exc_info:
            validator.validate(IntStrModel, df)

        error_msg = str(exc_info.value)
        assert 'int_col' in error_msg
        assert 'int' in error_msg

    def test_polars_validate_dtypes_with_lazy_frame(self) -> None:
        """Test that dtype validation works with LazyFrame."""

        config = TyframeColumnValidation(validate_dtypes=True)
        validator = LazyPolarsValidator(config=config)
        df = pl.LazyFrame(
            {
                'int_col': [1, 2, 3],
                'str_col': ['a', 'b', 'c'],
            }
        )

        result = validator.validate(IntStrModel, df)
        assert result is not None
