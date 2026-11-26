"""Validation benchmark: times tyframe validation of raw pandas and polars dataframes."""

from functools import partial

from benchmark.common import (
    DEFAULT_ROWS,
    DROP_COLUMNS,
    EXTRA_COLUMNS,
    BenchmarkResult,
    PandasDataFrameBuilder,
    PolarsDataFrameBuilder,
    build_raw_pandas_df,
    build_raw_polars_df,
    time_repeats,
)
from benchmark.generated.pandas import C1Pd, C10Pd, C100Pd
from benchmark.generated.polars import C1Pl, C10Pl, C100Pl
from tyframe.validation.config import TyframeColumnValidation
from tyframe.validation.pandas import PandasValidator
from tyframe.validation.polars import PolarsValidator

PANDAS_WRAPPERS = {1: C1Pd, 10: C10Pd, 100: C100Pd}
POLARS_WRAPPERS = {1: C1Pl, 10: C10Pl, 100: C100Pl}

type PandasWrapperClass = type[C1Pd | C10Pd | C100Pd]
type PolarsWrapperClass = type[C1Pl | C10Pl | C100Pl]

SCENARIOS = (
    (TyframeColumnValidation(validate_dtypes=True), 0, 0),
    (TyframeColumnValidation(validate_dtypes=False), 0, 0),
    (TyframeColumnValidation(validate_dtypes=False, drop_extra_columns=True), EXTRA_COLUMNS, 0),
    (TyframeColumnValidation(validate_dtypes=False, fill_with_default=True), 0, DROP_COLUMNS),
    (
        TyframeColumnValidation(
            validate_dtypes=False,
            fill_with_default=True,
            drop_extra_columns=True,
        ),
        EXTRA_COLUMNS,
        DROP_COLUMNS,
    ),
)


def benchmark_pandas(
    config: TyframeColumnValidation,
    build_dataframe_method: PandasDataFrameBuilder,
    wrapper_cls: PandasWrapperClass,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark validation of a pandas dataframe."""
    df = build_dataframe_method(wrapper_cls.model)
    validator = PandasValidator(column_config=config)
    mean_ms, std_ms = time_repeats(lambda: wrapper_cls(df, validator), repeat)

    return BenchmarkResult(
        library='pandas',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=mean_ms,
        std_ms=std_ms,
        config=config,
    )


def benchmark_polars(
    config: TyframeColumnValidation,
    build_dataframe_method: PolarsDataFrameBuilder,
    wrapper_cls: PolarsWrapperClass,
    repeat: int,
) -> BenchmarkResult:
    """Benchmark validation of a polars dataframe."""
    df = build_dataframe_method(wrapper_cls.model)
    validator = PolarsValidator(column_config=config)
    mean_ms, std_ms = time_repeats(lambda: wrapper_cls(df, validator), repeat)

    return BenchmarkResult(
        library='polars',
        n_col=len(df.columns),
        n_row=len(df),
        mean_ms=mean_ms,
        std_ms=std_ms,
        config=config,
    )


def run_validation_benchmark(repeat: int) -> list[BenchmarkResult]:
    """Run the validation benchmark over all scenarios, wrappers and row counts."""
    results: list[BenchmarkResult] = []
    for config, extra_columns, drop_columns in SCENARIOS:
        results.extend(
            benchmark_pandas(
                config,
                partial(
                    build_raw_pandas_df,
                    n_rows=n_rows,
                    add_extra_columns=extra_columns,
                    drop_columns=drop_columns,
                ),
                wrapper_cls,
                repeat,
            )
            for wrapper_cls in PANDAS_WRAPPERS.values()
            for n_rows in DEFAULT_ROWS
        )
        results.extend(
            benchmark_polars(
                config,
                partial(
                    build_raw_polars_df,
                    n_rows=n_rows,
                    add_extra_columns=extra_columns,
                    drop_columns=drop_columns,
                ),
                wrapper_cls,
                repeat,
            )
            for wrapper_cls in POLARS_WRAPPERS.values()
            for n_rows in DEFAULT_ROWS
        )
    return results
