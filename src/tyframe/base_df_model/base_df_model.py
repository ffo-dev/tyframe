from abc import ABCMeta
from typing import Any, ClassVar, Generic, cast, override

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

from tyframe.tagging import BaseColumnTags, TagT, invert_column_tags


class BaseDfModel(BaseModel, Generic[TagT], metaclass=ABCMeta):  # noqa: UP046
    """Base class to create a model to validate and build dataframes.

    Generic over the tag type: subclass as `BaseDfModel[MyTag]` to allow
    annotating fields with a custom tag type via `BaseColumnTags[MyTag]`.
    Bare `BaseDfModel` defaults to `TyframeTag`.
    """

    columns: ClassVar[list[str]]
    defaults: ClassVar[dict[str, Any]]  # pyright:ignore[reportExplicitAny]
    columns_by_tag: ClassVar[dict[str, list[str]]]

    @override
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:  # pyright:ignore[reportExplicitAny, reportAny]
        cls.columns = list(cls.model_fields.keys())
        cls.defaults = {
            k: v.default  # pyright:ignore[reportAny]
            for k, v in cls.model_fields.items()
            if not isinstance(v.default, PydanticUndefinedType)  # pyright:ignore[reportAny]
        }
        cls.columns_by_tag = cast(
            'dict[str, list[str]]',
            invert_column_tags(
                {
                    col_name: cast('BaseColumnTags[TagT]', meta)
                    for col_name, field_info in cls.model_fields.items()
                    for meta in field_info.metadata
                    if isinstance(meta, BaseColumnTags)
                }
            ),
        )
        super().__pydantic_init_subclass__(**kwargs)

    @classmethod
    def columns_with_tag(cls, tag: TagT) -> list[str]:
        """Return the names of all columns annotated with the given tag.

        Fields are tagged via `Annotated[<type>, BaseColumnTags(...)]`.

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
