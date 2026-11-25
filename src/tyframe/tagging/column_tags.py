from collections import UserList
from collections.abc import Iterable
from typing import Literal

MappingTag = Literal['map_key', 'map_value']
JoinTag = Literal['join_key', 'join_value']
TyframeTag = MappingTag | JoinTag


class TyframeColumnTags(UserList[TyframeTag]):
    def __init__(self, tags: Iterable[TyframeTag] | TyframeTag | None = None) -> None:
        match tags:
            case None:
                super().__init__([])
            case str():
                super().__init__([tags])
            case _:
                super().__init__(tags)

    def add_tag(self, tag: TyframeTag) -> None:
        if tag not in self:
            self.append(tag)

    def remove_tag(self, tag: TyframeTag) -> None:
        if tag in self:
            self.remove(tag)
