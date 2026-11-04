from tyframe.base_df_model import BaseDfModel


class OneColModel(BaseDfModel):
    a: int


class TwoColModel(OneColModel):
    b: str


class OtherExample(BaseDfModel):
    yaba: str
