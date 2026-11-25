from typing import Annotated

import pandas as pd
import polars as pl
import pytest

from tyframe.base_df_model import BaseDfModel
from tyframe.tagging import TyframeColumnConfig
from tyframe.validation.config import TyframeRowValidation
from tyframe.validation.exceptions import DuplicatePrimaryKeyError
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import LazyPolarsValidator, PolarsValidator


class UserModel(BaseDfModel):
    id: Annotated[int, TyframeColumnConfig(pk=True)]
    name: str


class NoPkModel(BaseDfModel):
    id: int
    name: str


class OrderModel(BaseDfModel):
    order_id: Annotated[int, TyframeColumnConfig(pk=True)]
    line_no: Annotated[int, TyframeColumnConfig(pk=True)]
    qty: int


def test_unique_pk_passes() -> None:
    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['a', 'b', 'c']})

    result = PandasValidator().validate(UserModel, df)

    assert result.equals(df)


def test_duplicate_pk_raises() -> None:
    df = pd.DataFrame({'id': [1, 1, 2], 'name': ['a', 'b', 'c']})

    with pytest.raises(DuplicatePrimaryKeyError, match='id'):
        PandasValidator().validate(UserModel, df)


def test_duplicate_pk_allowed_when_disabled() -> None:
    df = pd.DataFrame({'id': [1, 1, 2], 'name': ['a', 'b', 'c']})
    validator = PandasValidator(row_config=TyframeRowValidation(validate_pk_uniqueness=False))

    result = validator.validate(UserModel, df)

    assert result.equals(df)


def test_no_pk_columns_does_nothing() -> None:
    df = pd.DataFrame({'id': [1, 1, 2], 'name': ['a', 'b', 'c']})

    result = PandasValidator().validate(NoPkModel, df)

    assert result.equals(df)


def test_composite_pk_uniqueness() -> None:
    unique_df = pd.DataFrame({'order_id': [1, 1, 2], 'line_no': [1, 2, 1], 'qty': [5, 6, 7]})
    PandasValidator().validate(OrderModel, unique_df)

    duplicate_df = pd.DataFrame({'order_id': [1, 1], 'line_no': [1, 1], 'qty': [5, 6]})
    with pytest.raises(DuplicatePrimaryKeyError, match='line_no'):
        PandasValidator().validate(OrderModel, duplicate_df)


def test_polars_duplicate_pk_raises() -> None:
    df = pl.DataFrame({'id': [1, 1, 2], 'name': ['a', 'b', 'c']})

    with pytest.raises(DuplicatePrimaryKeyError, match='id'):
        PolarsValidator().validate(UserModel, df)


def test_lazy_polars_duplicate_pk_raises() -> None:
    lf = pl.LazyFrame({'id': [1, 1, 2], 'name': ['a', 'b', 'c']})

    with pytest.raises(DuplicatePrimaryKeyError, match='id'):
        LazyPolarsValidator().validate(UserModel, lf)


def test_lazy_polars_unique_pk_passes() -> None:
    lf = pl.LazyFrame({'id': [1, 2, 3], 'name': ['a', 'b', 'c']})

    result = LazyPolarsValidator().validate(UserModel, lf)

    assert isinstance(result, pl.LazyFrame)
