from collections import UserList
from collections.abc import Iterable
from typing import Literal

from typing_extensions import TypeVar

MappingTag = Literal['map_key', 'map_value']
JoinTag = Literal['join_key', 'join_value']
PrimaryKeyTag = Literal['primary_key']
TyframeTag = MappingTag | JoinTag | PrimaryKeyTag

TagT = TypeVar('TagT', bound=str, default=TyframeTag)


class BaseColumnTags(UserList[TagT]):
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


class TyframeColumnTags(BaseColumnTags[TyframeTag]):
    pass
