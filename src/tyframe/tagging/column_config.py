from dataclasses import dataclass


@dataclass(frozen=True)
class TyframeColumnConfig:
    """Per-column configuration, annotatable via `Annotated[<type>, TyframeColumnConfig(...)]`."""

    pk: bool = False
