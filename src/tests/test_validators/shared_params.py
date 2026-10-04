import pytest

from tests.test_validators.constants import TEST_FILE_PATH
from tests.test_validators.example_models import ExampleModel, ModelWithDefault
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.exceptions.column_exceptions import (
    ExtraColumnsError,
    MissingColumnsError,
)

EXAMPLE_MODEL_PATH = TEST_FILE_PATH / "example_model"
MODEL_WITH_DEFAULTL_PATH = TEST_FILE_PATH / "model_with_default"

SUCCESSFULL_VALIDATION = [
    pytest.param(
        EXAMPLE_MODEL_PATH / "input.csv",
        ExampleModel,
        EXAMPLE_MODEL_PATH / "expected.csv",
        TyframeValidationConfig(),
    ),
    pytest.param(
        EXAMPLE_MODEL_PATH / "input_extra_col.csv",
        ExampleModel,
        EXAMPLE_MODEL_PATH / "expected.csv",
        TyframeValidationConfig(drop_extra_columns=True),
    ),
    pytest.param(
        MODEL_WITH_DEFAULTL_PATH / "input_with_no_col.csv",
        ModelWithDefault,
        MODEL_WITH_DEFAULTL_PATH / "expected_with_no_col.csv",
        TyframeValidationConfig(fill_with_default=True),
    ),
    pytest.param(
        MODEL_WITH_DEFAULTL_PATH / "input_with_one_col.csv",
        ModelWithDefault,
        MODEL_WITH_DEFAULTL_PATH / "expected_with_one_col.csv",
        TyframeValidationConfig(fill_with_default=True),
    ),
]

RAISE_ERROR_VALIDATION = [
    pytest.param(
        EXAMPLE_MODEL_PATH / "input_extra_col.csv",
        ExampleModel,
        TyframeValidationConfig(drop_extra_columns=False),
        ExtraColumnsError,
    ),
    pytest.param(
        EXAMPLE_MODEL_PATH / "input_missing_col.csv",
        ExampleModel,
        TyframeValidationConfig(drop_extra_columns=False),
        MissingColumnsError,
    ),
]
