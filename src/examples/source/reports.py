from tyframe.base_df_model import BaseDfModel


class RevenueByRegion(BaseDfModel):
    region: str
    revenue: float


class CustomerSpendSummary(BaseDfModel):
    id: int
    name: str
    last_name: str
    net_spend: float
