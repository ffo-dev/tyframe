# Tyframe

Tyframe generates typed pandas/polars DataFrame wrappers from your Python classes.

## Installation

```bash
pip install tyframe
```

## Usage

```bash
tyframe generate-typed-wrapper --input-path <source_dir> --output-path <output_dir> --df-type <df_type> --class-suffix <suffix> [--config-path <config.yml>]
```

Run `tyframe generate-typed-wrapper --help` for the full option list. If you omit a required option, the CLI prompts for it interactively (invalid answers, e.g. an unknown `--df-type` or a nonexistent `--input-path`, are re-prompted).

| Option | Required | Default | Description |
| --- | --- | --- | --- |
| `--input-path` | yes | — | Python file or directory with the `BaseDfModel` subclasses to wrap. |
| `--output-path` | yes | — | Directory the generated wrapper files are written to. |
| `--config-path` | no | `tyframe_config.yaml` | Generator config file (YAML or JSON): indentation size, column property suffix. |
| `--df-type` | yes | — | DataFrame library: `pandas`, `polars`, or `lazy_polars`. |
| `--class-suffix` | yes | — | Suffix appended to each model name, e.g. `Pl` -> `TransactionPl`. |

Example:

```bash
tyframe generate-typed-wrapper --input-path src/classes --output-path src/generated --config-path tyframe_config.yml --df-type pandas --class-suffix Pd
```

## Generation example

Input — a plain model:

```python
from tyframe.base_df_model import BaseDfModel


class Transaction(BaseDfModel):
    customer_id: int
    amount: float
    region: str
```

Generate the wrapper:

```bash
tyframe generate-typed-wrapper --input-path src/models --output-path src/generated --config-path tyframe_config.yml --df-type polars --class-suffix Pl
```

Output — a typed wrapper with the model bound as its signature:

```python
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class TransactionPl(TypedPolarsDataFrame[Transaction]):
    model: type[Transaction] = Transaction
    customer_id: str = 'customer_id'
    amount: str = 'amount'
    region: str = 'region'

    @property
    def customer_id_col(self) -> pl.Series:
        return self._df[self.customer_id]

    @property
    def amount_col(self) -> pl.Series:
        return self._df[self.amount]

    @property
    def region_col(self) -> pl.Series:
        return self._df[self.region]

    #### CODE-GEN END

    def big_transactions(self, min_amount: float) -> Self:
        """Filter and sort; wrapper operations return the same typed wrapper, so calls chain."""
        filtered = self.filter(pl.col(self.amount) > min_amount)
        return filtered.sort(self.amount, ascending=False)
```

## Migrating existing DataFrames

Already have raw pandas/polars dataframes (loaded from CSV, a database, ...) and want typed wrappers for them? Kickstart the migration by generating a `BaseDfModel` straight from the dataframe — no need to write the model by hand. `PolarsModelGenerator` / `PandasModelGenerator` map each column's dtype to a Python type via the dtype mapping:

```python
from pathlib import Path

import polars as pl

from tyframe.code_gen.polars.polars_model_generator import PolarsModelGenerator
from tyframe.code_gen.pydantic_model_generator import PydanticModelGeneratorConfig

df = pl.read_csv('transactions.csv')  # any existing polars DataFrame

generator = PolarsModelGenerator(PydanticModelGeneratorConfig(), generated_class_suffix='')
generator.generate_model_file(df, Path('src/models'), 'Transaction')
```

This writes `src/models/transaction.py`:

```python
from tyframe.base_df_model.base_df_model import BaseDfModel

class Transaction(BaseDfModel):
    customer_id: int
    amount: float
    region: str
```

(`generate_model_class(df, 'Transaction')` returns the same code as a string if you prefer to inspect or post-process it. Use `PandasModelGenerator` for pandas dataframes.)

Then generate the wrapper with the CLI as usual — run it from your project root with the models importable, e.g. `PYTHONPATH=src`:

```bash
PYTHONPATH=src tyframe generate-typed-wrapper --input-path src/models --output-path src/generated --df-type polars --class-suffix Pl
```

Now onboard the existing dataframe: wrap it once and you get validation plus typed column access everywhere:

```python
import polars as pl

from generated import TransactionPl
from tyframe.validation.polars import PolarsValidator

df = pl.read_csv('transactions.csv')
typed = TransactionPl(df, PolarsValidator())  # validates columns/dtypes against Transaction

typed.amount_col        # pl.Series — typed access to the amount column
typed.filter(pl.col(typed.amount) > 100)   # still a TransactionPl, calls chain
```

## Validation

Wrappers validate a raw dataframe against the model when constructed. Tune the behavior with `TyframeValidationConfig` — all flags default to `False`:

```python
import polars as pl

from tyframe.validation.config import TyframeValidationConfig
from tyframe.validation.polars import PolarsValidator

# default: strict — extra or missing columns raise ExtraColumnsError / MissingColumnsError
strict = PolarsValidator()

# lenient: columns the model does not declare are dropped instead of raising
drop_extra = PolarsValidator(config=TyframeValidationConfig(drop_extra_columns=True))

# fill columns that have a model default (e.g. `region: str = 'EU'`);
# missing columns without a default still raise MissingColumnsWithoutDefaultError
fill_defaults = PolarsValidator(config=TyframeValidationConfig(fill_with_default=True))

# also check column dtypes against the model field types (raises DtypeMismatchError)
check_dtypes = PolarsValidator(config=TyframeValidationConfig(validate_dtypes=True))

df = pl.DataFrame({'customer_id': [1], 'amount': [120.0], 'region': ['EU'], 'note': ['x']})
TransactionPl(df, drop_extra)  # 'note' column is dropped
TransactionPl(df, strict)  # raises ExtraColumnsError
```

Flags can be combined, e.g. `TyframeValidationConfig(drop_extra_columns=True, validate_dtypes=True)`. `PandasValidator` and `LazyPolarsValidator` accept the same config.

### Performance

Validation is lightweight: the cost scales with the **number of columns, not the number of rows**. 


`drop_extra_columns=True`:

| cols \ rows | 100 | 10,000 | 1,000,000 |
| --- | --- | --- | --- |
| 11 | 0.012 | 0.012 | 0.011 |
| 20 | 0.064 | 0.055 | 0.056 |
| 110 | 0.153 | 0.152 | 0.149 |

`fill_with_default=True`:

| cols \ rows | 100 | 10,000 | 1,000,000 |
| --- | --- | --- | --- |
| 1 | 0.001 | 0.001 | 0.001 |
| 5 | 0.060 | 0.057 | 0.057 |
| 95 | 0.083 | 0.083 | 0.087 |

(Combined `drop_extra_columns=True, fill_with_default=True`: 0.232 / 0.226 / 0.227 ms at 105 cols — still flat across rows.)

With `drop_extra_columns=True`, validating a 110-column polars frame costs ~0.15 ms whether it holds 100 rows or 1,000,000:

```python
import polars as pl

from tyframe.validation.polars import PolarsValidator

validator = PolarsValidator()
small = pl.DataFrame({'customer_id': range(100), 'amount': [1.0] * 100, 'region': ['EU'] * 100})
big = pl.DataFrame({'customer_id': range(1_000_000), 'amount': [1.0] * 1_000_000, 'region': ['EU'] * 1_000_000})

validator.validate(Transaction, small)  # ~0.001 ms
validator.validate(Transaction, big)  # ~0.001 ms — same: cost is per column, not per row
```

The project maintains a benchmark script to verify that future changes will not degrade the performance.
YOu can run it with `poe benchmark` to get the expected performance on your machine.