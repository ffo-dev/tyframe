from pathlib import Path

from typer import echo

from tyframe.cli.cli_app import app


@app.command()
def generate_model_from_file(
    *,
    input_path: Path,
    file_suffix: str,
) -> None:
    echo(f'generating for input_path {input_path} and file suffix {file_suffix}')
