from collections.abc import Callable
from pathlib import Path

import pytest

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.base_validator import BaseValidator, DataFrameType
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.exceptions import BaseTyframeValidationException


def successful_validation(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    expected_data_path: Path,
    validator: BaseValidator[DataFrameType],
    reader: Callable[[Path], DataFrameType],
    comparator: Callable[[DataFrameType, DataFrameType], None],
    validation_config: TyframeValidationConfig,
) -> None:
    input_df = reader(input_data_path)

    validated_df = validator.validate(model_type, input_df, validation_config)

    expected_df = reader(expected_data_path)

    comparator(validated_df, expected_df)


def validation_with_raise(
    input_data_path: Path,
    model_type: type[BaseDfModel],
    validator: BaseValidator[DataFrameType],
    reader: Callable[[Path], DataFrameType],
    expected_exception: type[BaseTyframeValidationException],
    validation_config: TyframeValidationConfig,
) -> None:
    input_df = reader(input_data_path)

    with pytest.raises(expected_exception):
        _ = validator.validate(model_type, input_df, validation_config)
