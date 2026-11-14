import polars as pl

from examples.source.models import Customer
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class CustomerPl(TypedPolarsDataFrame[Customer]):
    model: type[Customer] = Customer
    id: str = 'id'
    name: str = 'name'
    last_name: str = 'last_name'

    @property
    def id_col(self) -> pl.Series:
        return self._df[self.id]

    @property
    def name_col(self) -> pl.Series:
        return self._df[self.name]

    @property
    def last_name_col(self) -> pl.Series:
        return self._df[self.last_name]


#### CODE-GEN END
