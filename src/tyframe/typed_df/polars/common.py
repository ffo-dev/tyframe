from collections.abc import Sequence


def flip_bool(v: bool | Sequence[bool]) -> bool | Sequence[bool]:
    if isinstance(v, bool):
        return not v
    return tuple(not el for el in v)
