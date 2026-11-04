from collections.abc import Iterable

from tyframe.validation.exceptions.base_validation_exception import (
    BaseTyframeValidationError,
)


class MissingColumnsError(BaseTyframeValidationError):
    def __init__(
        self,
        *,
        expected_columns: Iterable[str],
        missing_columns: Iterable[str],
    ) -> None:

        rows = [
            f'Expected: {sorted(expected_columns)}',
            f'Missing : {sorted(missing_columns)}',
        ]

        super().__init__('\n'.join(rows))


class MissingColumnsWithoutDefaultError(BaseTyframeValidationError):
    def __init__(
        self,
        *,
        missing_columns: Iterable[str],
        missing_without_default: Iterable[str],
    ) -> None:

        rows = [
            f'Missing   : {sorted(missing_columns)}',
            f'No Default: {sorted(missing_without_default)}',
        ]

        super().__init__('\n'.join(rows))


class ExtraColumnsError(BaseTyframeValidationError):
    def __init__(
        self,
        *,
        expected_columns: Iterable[str],
        extra: Iterable[str],
    ) -> None:

        rows = [
            f'Expected: {sorted(expected_columns)}',
            f'Extra   : {sorted(extra)}',
        ]
        super().__init__('\n'.join(rows))
