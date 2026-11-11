from pathlib import Path
from typing import Self

import yaml
from pydantic import BaseModel, computed_field


class BaseCodeGeneratorConfig(BaseModel):
    """Base configuration for code generators."""

    indentation_size: int = 4

    code_gen_hook: str = 'CODE-GEN'

    @computed_field
    @property
    def indentation(self) -> str:
        """Get the indentation string based on indentation_size."""
        return ' ' * self.indentation_size

    @computed_field
    @property
    def code_gen_start(self) -> str:
        return f'#### {self.code_gen_hook} START'

    @computed_field
    @property
    def code_gen_end(self) -> str:
        return f'#### {self.code_gen_hook} END'

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """Load configuration from a file.

        Args:
            path: Path to the configuration file.

        Returns:
            An instance of the configuration class.

        Raises:
            ValueError: If the file format is not supported.
        """
        match path.suffix:
            case '.yaml' | '.yml' | '.json':
                raw_dict = yaml.safe_load(path.read_text())  # pyright:ignore[reportAny]
                return cls(**raw_dict)  # pyright:ignore[reportAny]
            case _:
                msg = f'Unsupported file format: {path.suffix}'
                raise ValueError(msg)
