from tyframe.base_df_model.base_df_model import BaseDfModel


class ExampleModel(BaseDfModel):
    a: int
    b: str


class ModelWithDefault(BaseDfModel):
    a: int
    b: int = 3
    c: str = "z"