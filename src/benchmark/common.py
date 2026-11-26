"""Shared helpers for the tyframe benchmarks."""

import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import polars as pl
import typer

from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.validation.config import BaseTyframeValidationConfig

DEFAULT_ROWS = [100, 10_000, 1_000_000]
EXTRA_COLUMNS = 10
DROP_COLUMNS = 5

type PandasDataFrameBuilder = Callable[[type[BaseDfModel]], pd.DataFrame]
type PolarsDataFrameBuilder = Callable[[type[BaseDfModel]], pl.DataFrame]


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    library: str
    n_col: int
    n_row: int
    mean_ms: float
    std_ms: float
    config: BaseTyframeValidationConfig


def build_raw_polars_df(
    model: type[BaseDfModel],
    n_rows: int,
    add_extra_columns: int = 0,
    drop_columns: int = 0,
) -> pl.DataFrame:
    """Build a raw polars dataframe with valid model columns and extra columns."""
    remaining_model_columns = model.columns[: max(1, len(model.columns) - drop_columns)]
    df = pl.select(pl.int_range(0, n_rows, dtype=pl.Int32).alias(col) for col in remaining_model_columns)
    return df.with_columns(
        pl.int_range(0, n_rows, dtype=pl.Int32).alias(f'extra_{index + 1}') for index in range(add_extra_columns)
    )


def build_raw_pandas_df(
    model: type[BaseDfModel],
    n_rows: int,
    add_extra_columns: int = 0,
    drop_columns: int = 0,
) -> pd.DataFrame:
    """Build a raw pandas dataframe with valid model columns and extra columns."""
    remaining_model_columns = model.columns[: max(1, len(model.columns) - drop_columns)]
    columns = {col: range(n_rows) for col in remaining_model_columns}
    columns.update({f'extra_{index + 1}': range(n_rows) for index in range(add_extra_columns)})
    return pd.DataFrame(columns)


def time_repeats(
    fn: Callable[[], object],
    repeat: int,
) -> tuple[float, float]:
    """Run `fn` `repeat` times and return (mean ms, stddev ms)."""
    if repeat < 1:
        raise ValueError(repeat)
    times: list[float] = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        times.append(time.perf_counter() - start)
    return statistics.fmean(times) * 1000, statistics.pstdev(times) * 1000


def format_results(results: list[BenchmarkResult]) -> str:
    """Format benchmark results as a table."""
    return '\n'.join(
        [
            f'{"library":>7} | {"cols":>6} | {"rows":>9} | {"mean (ms)":>10} | {"std (ms)":>10} | config',
            *(
                f'{result.library:>7} | {result.n_col:>6} | {result.n_row:>9} | '
                f'{result.mean_ms:>10.3f} | {result.std_ms:>10.3f} | {result.config}'
                for result in results
            ),
        ]
    )


def show(results: list[BenchmarkResult]) -> None:
    """Print benchmark results."""
    typer.echo(format_results(results))


def save_results(
    sections: list[tuple[str, list[BenchmarkResult]]],
    save: Path,
) -> None:
    """Save titled benchmark result tables to a file."""
    save.write_text(
        '\n\n'.join(f'{title}\n{format_results(results)}' for title, results in sections) + '\n', encoding='utf-8'
    )
