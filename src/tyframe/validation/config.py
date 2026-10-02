from dataclasses import dataclass, field


@dataclass
class TyframeValidationConfig:
    drop_extra_columns: bool = field(default=False)
