from collections.abc import Iterable

from tyframe.validation.exceptions.base_validation_exception import (
    BaseTyframeValidationError,
)


class DuplicatePrimaryKeyError(BaseTyframeValidationError):
    def __init__(self, *, pk_columns: Iterable[str]) -> None:
        super().__init__(
            f'Duplicate values found in primary key column(s): {sorted(pk_columns)}',
        )
