from collections.abc import Callable
from pathlib import Path

import pytest

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator, DataFrameType
from tyframe.validation.exceptions import BaseTyframeValidationException

@pytest.mark.skip(reason='Base test to use for each validator')
def test_successful_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    expected_data_path: Path,
    validator: BaseValidator[DataFrameType],
    reader: Callable[[Path], DataFrameType],
    comparator: Callable[[DataFrameType, DataFrameType], None],
) -> None:
    input_df = reader(input_data_path)

    validated_df = validator.validate(model_type, input_df)

    expected_df = reader(expected_data_path)

    comparator(validated_df, expected_df)

@pytest.mark.skip(reason='Base test to use for each validator')
def test_validation_with_raise(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    validator: BaseValidator[DataFrameType],
    reader: Callable[[Path], DataFrameType],
    expected_exception: type[BaseTyframeValidationException],
) -> None:
    input_df = reader(input_data_path)

    with pytest.raises(expected_exception):
        _ = validator.validate(model_type, input_df)
