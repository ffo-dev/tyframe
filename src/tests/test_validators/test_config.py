import pytest

from tyframe.validation.config import TyframeValidationConfig


def test_subclass_with_only_bool_fields_is_allowed() -> None:

    class CustomConfig(TyframeValidationConfig):
        extra_check: bool = False

    config = CustomConfig(extra_check=True)

    assert config.extra_check is True
    assert config.drop_extra_columns is False


def test_subclass_with_non_bool_field_raises() -> None:
    with pytest.raises(TypeError, match='may only add boolean fields') as exc_info:
        type('BadConfig', (TyframeValidationConfig,), {'__annotations__': {'count': int}, 'count': 0})

    assert 'count' in str(exc_info.value)


def test_subclass_with_non_bool_field_no_default_raises() -> None:
    with pytest.raises(TypeError, match='may only add boolean fields'):
        type('BadConfig', (TyframeValidationConfig,), {'__annotations__': {'name': str}})
