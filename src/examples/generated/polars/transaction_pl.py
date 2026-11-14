import polars as pl
from examples.source.models import Transaction
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame

# I am another comment and should be kept


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

    def total(self) -> float:
        return sum(self.amount_col)
