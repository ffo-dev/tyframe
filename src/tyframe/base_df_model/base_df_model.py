from abc import ABCMeta
from typing import Any, ClassVar, cast, override

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

from tyframe.tagging.base_column_tags import BaseColumnTags, invert_column_tags
from tyframe.tagging.tags import TyframeTag


class BaseDfModel(BaseModel, metaclass=ABCMeta):
    """Base class to create a model to validate and build dataframes."""

    columns: ClassVar[list[str]]
    defaults: ClassVar[dict[str, Any]]  # pyright:ignore[reportExplicitAny]
    columns_by_tag: ClassVar[dict[TyframeTag, list[str]]]

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:  # pyright:ignore[reportExplicitAny, reportAny]
        cls.columns = list(cls.model_fields.keys())
        cls.defaults = {
            k: v.default  # pyright:ignore[reportAny]
            for k, v in cls.model_fields.items()
            if not isinstance(v.default, PydanticUndefinedType)  # pyright:ignore[reportAny]
        }
        cls.columns_by_tag = invert_column_tags(
            {
                col_name: cast('BaseColumnTags[TyframeTag]', meta)
                for col_name, field_info in cls.model_fields.items()
                for meta in field_info.metadata
                if isinstance(meta, BaseColumnTags)
            }
        )
        super().__pydantic_init_subclass__(**kwargs)

    @classmethod
    def columns_with_tag(cls, tag: TyframeTag) -> list[str]:
        """Return the names of all columns annotated with the given tag.

        Fields are tagged via `Annotated[<type>, TyframeColumnTags(...)]`.

        Args:
            tag: The tag to look for in the fields' annotated column tags.

        Returns:
            list[str]: Column names carrying the tag, in model field order.

        """
        return cls.columns_by_tag.get(tag, [])

    def to_record(self) -> dict[str, Any]:  # pyright:ignore[reportExplicitAny]
        """Convert the model instance to a record.

        Currently just a wrapper around model_dump, but can be extended/override
        in the future to add more functionality.
        """
        return self.model_dump()
