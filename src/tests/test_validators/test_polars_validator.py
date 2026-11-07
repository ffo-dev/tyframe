from pathlib import Path

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from tests.test_validators.constants import TEST_FILE_PATH
from tests.test_validators.shared_params import (
    RAISE_ERROR_VALIDATION,
    SUCCESSFULL_VALIDATION,
)
from tests.test_validators.utils import (
    successful_validation,
    validation_with_raise,
)
from tests.utils.readers import read_lazy_polars, read_polars
from tyframe.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.exceptions import (
    BaseTyframeValidationError,
)
from tyframe.validation.polars import LazyPolarsValidator, PolarsValidator

EXAMPLE_MODEL_PATH = TEST_FILE_PATH / 'example_model'


def strict_polars_comparator(
    left: pl.DataFrame | pl.LazyFrame,
    right: pl.DataFrame | pl.LazyFrame,
) -> None:
    assert_frame_equal(left, right)


def strict_polars_comparator_relaxed_columns(
    left: pl.DataFrame | pl.LazyFrame,
    right: pl.DataFrame | pl.LazyFrame,
) -> None:
    assert_frame_equal(
        left,
        right,
        check_column_order=False,
        check_dtypes=False,
    )


@pytest.mark.parametrize(
    (
        'input_data_path',
        'model_type',
        'expected_data_path',
        'validation_config',
    ),
    SUCCESSFULL_VALIDATION,
)
def test_polars_successful_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    expected_data_path: Path,
    validation_config: TyframeValidationConfig,
) -> None:
    successful_validation(
        input_data_path,
        model_type,
        expected_data_path,
        PolarsValidator(config=validation_config),
        read_polars,
        strict_polars_comparator_relaxed_columns,
    )


@pytest.mark.parametrize(
    ('input_data_path', 'model_type', 'validation_config', 'expected_error'),
    RAISE_ERROR_VALIDATION,
)
def test_polars_unsucessfull_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    validation_config: TyframeValidationConfig,
    expected_error: type[BaseTyframeValidationError],
) -> None:
    validation_with_raise(
        input_data_path,
        model_type,
        PolarsValidator(config=validation_config),
        read_polars,
        expected_error,
    )


@pytest.mark.parametrize(
    (
        'input_data_path',
        'model_type',
        'expected_data_path',
        'validation_config',
    ),
    SUCCESSFULL_VALIDATION,
)
def test_lazy_polars_successful_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    expected_data_path: Path,
    validation_config: TyframeValidationConfig,
) -> None:
    successful_validation(
        input_data_path,
        model_type,
        expected_data_path,
        LazyPolarsValidator(config=validation_config),
        read_lazy_polars,
        strict_polars_comparator_relaxed_columns,
    )


@pytest.mark.parametrize(
    ('input_data_path', 'model_type', 'validation_config', 'expected_error'),
    RAISE_ERROR_VALIDATION,
)
def test_lazy_polars_unsucessfull_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    validation_config: TyframeValidationConfig,
    expected_error: type[BaseTyframeValidationError],
) -> None:
    validation_with_raise(
        input_data_path,
        model_type,
        LazyPolarsValidator(config=validation_config),
        read_lazy_polars,
        expected_error,
    )
