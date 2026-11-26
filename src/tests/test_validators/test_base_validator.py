from tyframe.validation.config import TyframeColumnValidation, TyframeRowValidation
from tyframe.validation.pandas import PandasValidator


def test_validator_uses_default_configs_when_omitted() -> None:
    validator = PandasValidator()

    assert validator.column_config == TyframeColumnValidation()
    assert validator.row_config == TyframeRowValidation()


def test_validator_uses_default_configs_when_explicit_none() -> None:
    validator = PandasValidator(column_config=None, row_config=None)

    assert validator.column_config == TyframeColumnValidation()
    assert validator.row_config == TyframeRowValidation()


def test_validator_keeps_given_configs_as_is() -> None:
    column_config = TyframeColumnValidation(drop_extra_columns=True)
    row_config = TyframeRowValidation(validate_pk_uniqueness=False)

    validator = PandasValidator(column_config=column_config, row_config=row_config)

    assert validator.column_config is column_config
    assert validator.row_config is row_config
