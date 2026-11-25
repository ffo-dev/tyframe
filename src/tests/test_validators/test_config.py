from typing import cast

import pytest

from tyframe.validation.config import TyframeValidationConfig


def _and(a: TyframeValidationConfig, b: object) -> object:
    return cast('object', a & b)  # pyright:ignore[reportOperatorIssue]


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


def test_and_combines_field_by_field() -> None:
    a = TyframeValidationConfig(
        drop_extra_columns=True,
        fill_with_default=False,
        validate_dtypes=True,
    )
    b = TyframeValidationConfig(
        drop_extra_columns=True,
        fill_with_default=True,
        validate_dtypes=False,
    )

    result = a & b

    assert result.drop_extra_columns is True
    assert result.fill_with_default is False
    assert result.validate_dtypes is False


def test_or_combines_field_by_field() -> None:
    a = TyframeValidationConfig(
        drop_extra_columns=True,
        fill_with_default=False,
        validate_dtypes=True,
    )
    b = TyframeValidationConfig(
        drop_extra_columns=False,
        fill_with_default=True,
        validate_dtypes=False,
    )

    result = a | b

    assert result.drop_extra_columns is True
    assert result.fill_with_default is True
    assert result.validate_dtypes is True


def test_and_or_preserve_subclass_and_do_not_mutate_operands() -> None:

    class CustomConfig(TyframeValidationConfig):
        extra_check: bool = False

    a = CustomConfig(
        drop_extra_columns=True,
        fill_with_default=False,
        validate_dtypes=True,
        extra_check=True,
    )
    b = CustomConfig(
        drop_extra_columns=False,
        fill_with_default=True,
        validate_dtypes=False,
        extra_check=False,
    )

    and_result = a & b
    or_result = a | b

    assert type(and_result) is CustomConfig
    assert type(or_result) is CustomConfig
    assert and_result.drop_extra_columns is False
    assert and_result.fill_with_default is False
    assert and_result.validate_dtypes is False
    assert and_result.extra_check is False
    assert or_result.drop_extra_columns is True
    assert or_result.fill_with_default is True
    assert or_result.validate_dtypes is True
    assert or_result.extra_check is True
    assert a == CustomConfig(drop_extra_columns=True, fill_with_default=False, validate_dtypes=True, extra_check=True)
    assert b == CustomConfig(drop_extra_columns=False, fill_with_default=True, validate_dtypes=False, extra_check=False)


def test_and_with_non_config_raises_type_error() -> None:
    with pytest.raises(TypeError, match='unsupported operand'):
        _and(TyframeValidationConfig(), 5)
