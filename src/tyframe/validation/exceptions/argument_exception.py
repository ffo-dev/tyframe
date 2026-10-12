from abc import ABCMeta
from collections.abc import Sequence

from tyframe.validation.exceptions.base_validation_exception import (
    BaseTyframeValidationError,
)


class TyframeArgumentError(BaseTyframeValidationError, metaclass=ABCMeta):
    pass


class InvalidSkipValidationError(TyframeArgumentError):
    def __init__(self, expected_type: type[object]) -> None:
        super().__init__(
            f'skip_validation flag can only be used when input_data is a {expected_type.__name__} instance.',
        )


class InvalidInputTypesError(TyframeArgumentError):
    def __init__(self, input_type: type, valid_types: Sequence[str]) -> None:
        msg = f'Invalid input_type: {input_type.__name__}\nExpected {",".join(valid_types)}'
        super().__init__(msg)
