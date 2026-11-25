import pytest

from tests.test_validators.constants import TEST_FILE_PATH
from tests.test_validators.example_models import ExampleModel, ModelWithDefault
from tyframe.validation.config import TyframeColumnValidation
from tyframe.validation.exceptions.column_exceptions import (
    ExtraColumnsError,
    MissingColumnsError,
    MissingColumnsWithoutDefaultError,
)

EXAMPLE_MODEL_PATH = TEST_FILE_PATH / 'example_model'
MODEL_WITH_DEFAULT_PATH = TEST_FILE_PATH / 'model_with_default'

SUCCESSFULL_VALIDATION = [
    pytest.param(
        EXAMPLE_MODEL_PATH / 'input.csv',
        ExampleModel,
        EXAMPLE_MODEL_PATH / 'expected.csv',
        None,
    ),
    pytest.param(
        EXAMPLE_MODEL_PATH / 'input_extra_col.csv',
        ExampleModel,
        EXAMPLE_MODEL_PATH / 'expected.csv',
        TyframeColumnValidation(drop_extra_columns=True),
    ),
    pytest.param(
        MODEL_WITH_DEFAULT_PATH / 'input_with_no_col.csv',
        ModelWithDefault,
        MODEL_WITH_DEFAULT_PATH / 'expected_with_no_col.csv',
        TyframeColumnValidation(fill_with_default=True),
    ),
    pytest.param(
        MODEL_WITH_DEFAULT_PATH / 'input_with_one_col.csv',
        ModelWithDefault,
        MODEL_WITH_DEFAULT_PATH / 'expected_with_one_col.csv',
        TyframeColumnValidation(fill_with_default=True),
    ),
]

RAISE_ERROR_VALIDATION = [
    pytest.param(
        EXAMPLE_MODEL_PATH / 'input_extra_col.csv',
        ExampleModel,
        TyframeColumnValidation(drop_extra_columns=False),
        ExtraColumnsError,
    ),
    pytest.param(
        EXAMPLE_MODEL_PATH / 'input_missing_col.csv',
        ExampleModel,
        TyframeColumnValidation(drop_extra_columns=False),
        MissingColumnsError,
    ),
    pytest.param(
        MODEL_WITH_DEFAULT_PATH / 'input_missing_default_col.csv',
        ModelWithDefault,
        TyframeColumnValidation(fill_with_default=True),
        MissingColumnsWithoutDefaultError,
    ),
]
