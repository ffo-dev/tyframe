import polars as pl

from examples.source.reports import CustomerSpendSummary
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class CustomerSpendSummaryPl(TypedPolarsDataFrame[CustomerSpendSummary]):
    model: type[CustomerSpendSummary] = CustomerSpendSummary
    id: str = 'id'
    name: str = 'name'
    last_name: str = 'last_name'
    net_spend: str = 'net_spend'

    @property
    def id_col(self) -> pl.Series:
        return self._df[self.id]

    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]

    @property
    def last_name_col(self) -> pl.Series:
        return self._df[self.last_name]

    @property
    def net_spend_col(self) -> pl.Series:
        return self._df[self.net_spend]


#### CODE-GEN END
