from tyframe.base_df_model import BaseDfModel


class Customer(BaseDfModel):
    id: int
    name: str
    last_name: str


class Transaction(BaseDfModel):
    customer_id: int
    amount: float
    region: str


class Refund(BaseDfModel):
    id: int
    customer_id: int
    amount: float
    reason: str
