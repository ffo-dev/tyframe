import polars as pl

from examples.source.reports import RevenueByRegion
from tyframe.typed_df.polars.typed_polars import TypedPolarsDataFrame


#### CODE-GEN START
class RevenueByRegionPl(TypedPolarsDataFrame[RevenueByRegion]):
    model: type[RevenueByRegion] = RevenueByRegion
    region: str = 'region'
    revenue: str = 'revenue'

    @property
    def region_col(self) -> pl.Series:
        return self._df[self.region]

    @property
    def revenue_col(self) -> pl.Series:
        return self._df[self.revenue]


#### CODE-GEN END
