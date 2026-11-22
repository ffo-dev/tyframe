from typer import Typer

app = Typer(
    help='Generate typed pandas/polars DataFrame wrappers from pydantic models.',
    no_args_is_help=True,
)


@app.callback()
def callback() -> None:
    """Generate typed pandas/polars DataFrame wrappers from pydantic models."""
