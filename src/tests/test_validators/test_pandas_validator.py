from pathlib import Path

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from tests.test_validators.constants import TEST_FILE_PATH
from tests.test_validators.shared_params import (
    RAISE_ERROR_VALIDATION,
    SUCCESSFULL_VALIDATION,
)
from tests.test_validators.utils import (
    successful_validation,
    validation_with_raise,
)
from tests.utils.readers import read_pandas
from tyframe.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.exceptions import (
    BaseTyframeValidationException,
)
from tyframe.validation.pandas import PandasValidator

EXAMPLE_MODEL_PATH = TEST_FILE_PATH / "example_model"


def pandas_comparator(left: pd.DataFrame, right: pd.DataFrame) -> None:
    assert_frame_equal(left, right)


@pytest.mark.parametrize(
    (
        "input_data_path",
        "model_type",
        "expected_data_path",
        "validation_config",
    ),
    SUCCESSFULL_VALIDATION,
)
def test_pandas_successful_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    expected_data_path: Path,
    validation_config: TyframeValidationConfig,
) -> None:
    successful_validation(
        input_data_path,
        model_type,
        expected_data_path,
        PandasValidator(),
        read_pandas,
        pandas_comparator,
        validation_config,
    )


@pytest.mark.parametrize(
    ("input_data_path", "model_type", "validation_config", "expected_error"),
    RAISE_ERROR_VALIDATION,
)
def test_pandas_unsucessfull_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    validation_config: TyframeValidationConfig,
    expected_error: type[BaseTyframeValidationException],
):
    validation_with_raise(
        input_data_path,
        model_type,
        PandasValidator(),
        read_pandas,
        expected_error,
        validation_config,
    )
