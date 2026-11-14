import polars as pl

from examples.source.models import Refund
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class RefundPl(TypedPolarsDataFrame[Refund]):
    model: type[Refund] = Refund
    id: str = 'id'
    customer_id: str = 'customer_id'
    amount: str = 'amount'
    reason: str = 'reason'
    @property
    def id_col(self) -> pl.Series:
        return self._df[self.id]
    @property
    def customer_id_col(self) -> pl.Series:
        return self._df[self.customer_id]
    @property
    def amount_col(self) -> pl.Series:
        return self._df[self.amount]
    @property
    def reason_col(self) -> pl.Series:
        return self._df[self.reason]
#### CODE-GEN END
