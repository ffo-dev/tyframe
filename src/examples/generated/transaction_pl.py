from typing import Self

import polars as pl

from examples.generated.revenue_by_region_pl import RevenueByRegionPl
from examples.source.models import Transaction
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

    def revenue_by_region(self) -> RevenueByRegionPl:
        """Aggregate into a typed report; column names come from the generated attributes."""
        report = (
            self.df.group_by(self.region)
            .agg(pl.col(self.amount).sum().alias(RevenueByRegionPl.revenue))
            .sort(RevenueByRegionPl.revenue, descending=True)
        )
        return RevenueByRegionPl(report, self.validator)
