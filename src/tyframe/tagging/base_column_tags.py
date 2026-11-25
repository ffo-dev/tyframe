from abc import ABCMeta
from collections import UserList
from collections.abc import Iterable, Mapping

from typing_extensions import TypeVar

from tyframe.tagging.tags import TyframeTag

TagT = TypeVar('TagT', bound=str, default=TyframeTag)


class BaseColumnTags(UserList[TagT], metaclass=ABCMeta):
    def __init__(self, tags: Iterable[TagT] | TagT | None = None) -> None:
        match tags:
            case None:
                super().__init__([])
            case str():
                super().__init__([tags])
            case _:
                super().__init__(tags)

    def add_tag(self, tag: TagT) -> None:
        if tag not in self:
            self.append(tag)

    def remove_tag(self, tag: TagT) -> None:
        if tag in self:
            self.remove(tag)


def invert_column_tags(column_tags: Mapping[str, BaseColumnTags[TagT]]) -> dict[TagT, list[str]]:
    """Invert a column-to-tags mapping into a tag-to-columns mapping.

    Args:
        column_tags: Mapping of column name to the tags annotating it.

    Returns:
        dict[TagT, list[str]]: Mapping of each tag to the names of the columns carrying it,
            in the order the columns appear in the input.

    """
    result: dict[TagT, list[str]] = {}
    for col_name, tags in column_tags.items():
        for tag in tags:
            tagged_cols = result.setdefault(tag, [])
            if col_name not in tagged_cols:
                tagged_cols.append(col_name)
    return result
