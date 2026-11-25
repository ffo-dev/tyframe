from typing import Annotated

from tyframe.base_df_model import BaseDfModel
from tyframe.tagging import TyframeColumnTags


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
        id: Annotated[int, TyframeColumnTags('primary_key')]
        name: str
        price: Annotated[float, TyframeColumnTags(['unit_price', 'total_price'])]
        country: Annotated[str, TyframeColumnTags('country')]

    assert ExampleWithTags.columns_with_tag('primary_key') == ['id']
    assert ExampleWithTags.columns_with_tag('unit_price') == ['price']
    assert ExampleWithTags.columns_with_tag('total_price') == ['price']
    assert ExampleWithTags.columns_with_tag('country') == ['country']
    assert ExampleWithTags.columns_with_tag('map_key') == []
    assert ExampleWithTags.columns_by_tag == {
        'primary_key': ['id'],
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
