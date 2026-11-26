from typing import Annotated, Literal

from tyframe.base_df_model import BaseDfModel
from tyframe.tagging import BaseColumnTags, TyframeColumnTags, TyframeTag


class OneColModel(BaseDfModel):
    a: int


class TwoColModel(OneColModel):
    b: str


class OtherExample(BaseDfModel):
    yaba: str


class TaggedModel(BaseDfModel):
    id: Annotated[int, TyframeColumnTags('map_key')]
    price: Annotated[float, TyframeColumnTags(['unit_price', 'total_price'])]
    country: Annotated[str, TyframeColumnTags('country')]
    name: str


MyTag = TyframeTag | Literal['custom']


class CustomColumnTags(BaseColumnTags[MyTag]):
    pass


class CustomTagModel(BaseDfModel[MyTag]):
    a: Annotated[int, CustomColumnTags('custom')]
    b: Annotated[str, CustomColumnTags('map_key')]
    c: str
