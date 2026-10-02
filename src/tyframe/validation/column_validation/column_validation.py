from collections.abc import Sequence


def get_missing_columns(
    *,
    expected: Sequence[str],
    df_columns: Sequence[str],
) -> set[str]:
    return set(expected) - set(df_columns)


def get_extra_columns(
    *,
    expected: Sequence[str],
    df_columns: Sequence[str],
) -> set[str]:
    return set(df_columns) - set(expected)
