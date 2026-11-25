from abc import ABCMeta
from collections import UserList
from collections.abc import Iterable

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
