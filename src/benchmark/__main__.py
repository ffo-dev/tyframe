"""Benchmark CLI for tyframe dataframe validation.

Builds a raw polars dataframe that matches a model's schema (so it passes the
validator) and times how long validation takes.

Run from the repo root:

    poe benchmark
    uv run python -m benchmark --rows 100 --rows 1000000 --cols 100 --repeat 5
"""

import math
import time
from typing import Annotated

import polars as pl
import typer

from benchmark.generated import C1Pl, C10Pl, C100Pl
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.polars import PolarsValidator

app = typer.Typer(help='Benchmark tyframe validation of raw polars dataframes.')

WRAPPERS = {1: C1Pl, 10: C10Pl, 100: C100Pl}
DEFAULT_ROWS = [100, 10_000, 1_000_000]


def build_raw_df(
    model: type[BaseDfModel],
    n_rows: int,
) -> pl.DataFrame:
    """Build a raw polars dataframe with the model's columns and a valid dtype."""
    return pl.select(pl.int_range(0, n_rows, dtype=pl.Int32).alias(col) for col in model.columns)


def time_validation(
    model: type[BaseDfModel],
    n_rows: int,
    validator: PolarsValidator,
    repeat: int,
) -> float:
    """Return the best validation time in seconds over ``repeat`` runs."""
    df = build_raw_df(model, n_rows)
    best = math.inf
    for _ in range(repeat):
        start = time.perf_counter()
        validator.validate(model, df)
        best = min(best, time.perf_counter() - start)
    return best


@app.command()
def main(
    rows: Annotated[list[int] | None, typer.Option(help='Row counts to benchmark.')] = None,
    cols: Annotated[list[int] | None, typer.Option(help='Column counts to benchmark (subset of 1, 10, 100).')] = None,
    repeat: Annotated[int, typer.Option(help='Runs per case; the best time is reported.')] = 3,
) -> None:
    row_counts = rows or DEFAULT_ROWS
    cases = {n_cols: wrapper_cls for n_cols, wrapper_cls in WRAPPERS.items() if cols is None or n_cols in cols}
    validator = PolarsValidator(config=TyframeValidationConfig(validate_dtypes=True))

    typer.echo(f'{"cols":>6} | {"rows":>9} | {"validate (s)":>13}')
    for n_cols, wrapper_cls in cases.items():
        for n_rows in row_counts:
            elapsed = time_validation(wrapper_cls.model, n_rows, validator, repeat)
            typer.echo(f'{n_cols:>6} | {n_rows:>9} | {elapsed:>13.6f}')


if __name__ == '__main__':
    app()
