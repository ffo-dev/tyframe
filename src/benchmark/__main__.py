"""Benchmark CLI for tyframe dataframe validation and pk checks.

Runs the validation benchmark (raw pandas/polars dataframes timed through the
validator, reported as mean and stddev in milliseconds) and the pk-check benchmark
(primary-key uniqueness on/off, expected to scale with the number of rows).

Run from the repo root:

    poe benchmark
    uv run python -m benchmark --repeat 5
"""

from pathlib import Path
from typing import Annotated

import typer

from benchmark.common import save_results, show
from benchmark.pk_check_benchmark import run_pk_check_benchmark
from benchmark.validation_benchmark import run_validation_benchmark

app = typer.Typer(help='Benchmark tyframe validation of raw pandas and polars dataframes.')


@app.command()
def main(
    repeat: Annotated[
        int,
        typer.Option(help='Runs per case; mean and stddev in ms are reported.'),
    ] = 1000,
    save: Annotated[
        Path | None,
        typer.Option(help='Optional file path to save benchmark results.'),
    ] = None,
) -> None:
    sections = [
        ('Validation benchmark', run_validation_benchmark(repeat)),
        ('PK uniqueness check benchmark', run_pk_check_benchmark(repeat)),
    ]
    for title, results in sections:
        typer.echo(title)
        show(results)
    if save is not None:
        save_results(sections, save)


if __name__ == '__main__':
    app()
