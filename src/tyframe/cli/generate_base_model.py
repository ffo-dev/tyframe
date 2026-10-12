from pathlib import Path

from tyframe.cli.cli_app import app


@app.command()
def generate_model_from_file(
    *,
    input_path: Path,  # pyright:ignore[reportUnusedParameter]
    file_suffix: str, # pyright:ignore[reportUnusedParameter]
) -> None:
    raise NotImplementedError
