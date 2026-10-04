from collections.abc import Iterable


def get_missing_columns(
    *,
    expected: Iterable[str],
    df_columns: Iterable[str],
) -> set[str]:
    return set(expected) - set(df_columns)


def get_extra_columns(
    *,
    expected: Iterable[str],
    df_columns: Iterable[str],
) -> set[str]:
    return set(df_columns) - set(expected)
