from typing import Annotated, Literal

from tyframe.base_df_model import BaseDfModel
from tyframe.tagging import BaseColumnTags, TyframeColumnConfig, TyframeColumnTags, TyframeTag

MyTag = TyframeTag | Literal['custom']


class CustomColumnTags(BaseColumnTags[MyTag]):
    pass


def test_collect_col_names() -> None:

    class Example(BaseDfModel):
        col1: str
        col2: int

    assert Example.columns == ['col1', 'col2']
    assert 'col3' not in Example.columns


def test_collect_defaults() -> None:

    class ExampleWithDefault(BaseDfModel):
        a: str
        b: int = 2

    assert ExampleWithDefault.columns == ['a', 'b']
    assert ExampleWithDefault.defaults == {'b': 2}


def test_columns_with_tag() -> None:

    class ExampleWithTags(BaseDfModel):
        id: Annotated[int, TyframeColumnTags('map_key')]
        name: str
        price: Annotated[float, TyframeColumnTags(['unit_price', 'total_price'])]
        country: Annotated[str, TyframeColumnTags('country')]

    assert ExampleWithTags.columns_with_tag('map_key') == ['id']
    assert ExampleWithTags.columns_with_tag('unit_price') == ['price']
    assert ExampleWithTags.columns_with_tag('total_price') == ['price']
    assert ExampleWithTags.columns_with_tag('country') == ['country']
    assert ExampleWithTags.columns_with_tag('join_key') == []
    assert ExampleWithTags.columns_by_tag == {
        'map_key': ['id'],
        'unit_price': ['price'],
        'total_price': ['price'],
        'country': ['country'],
    }


def test_columns_by_tag_empty_when_no_tags() -> None:

    class Example(BaseDfModel):
        col1: str
        col2: int

    assert Example.columns_by_tag == {}


def test_columns_by_tag_multiple_columns_with_same_tag() -> None:

    class Example(BaseDfModel):
        key_a: Annotated[int, TyframeColumnTags('map_key')]
        key_b: Annotated[str, TyframeColumnTags('map_key')]
        other: str

    assert Example.columns_by_tag == {'map_key': ['key_a', 'key_b']}
    assert Example.columns_with_tag('map_key') == ['key_a', 'key_b']


def test_subclass_with_extended_tag_type() -> None:

    class CustomModel(BaseDfModel[MyTag]):
        a: Annotated[int, CustomColumnTags('custom'), TyframeColumnConfig(pk=True)]
        b: Annotated[str, CustomColumnTags('map_key')]
        c: str

    assert CustomModel.columns_by_tag == {'custom': ['a'], 'map_key': ['b']}
    assert CustomModel.columns_with_tag('custom') == ['a']
    assert CustomModel.columns_with_tag('map_key') == ['b']
    assert CustomModel.primary_keys == ['a']


def test_primary_keys() -> None:

    class Example(BaseDfModel):
        id: Annotated[int, TyframeColumnConfig(pk=True)]
        tenant_id: Annotated[int, TyframeColumnConfig(pk=True)]
        name: Annotated[str, TyframeColumnConfig()]
        other: str

    assert Example.primary_keys == ['id', 'tenant_id']


def test_primary_keys_empty_by_default() -> None:

    class Example(BaseDfModel):
        col1: str

    assert Example.primary_keys == []


def test_primary_keys_combined_with_tags() -> None:

    class Example(BaseDfModel):
        id: Annotated[int, TyframeColumnConfig(pk=True), TyframeColumnTags('map_key')]
        name: str

    assert Example.primary_keys == ['id']
    assert Example.columns_by_tag == {'map_key': ['id']}
    assert Example.columns_with_tag('map_key') == ['id']
