from typing import Literal

from tyframe.tagging import BaseColumnTags, TyframeColumnTags, TyframeTag, invert_column_tags

MyTag = TyframeTag | Literal['custom']


class CustomColumnTags(BaseColumnTags[MyTag]):
    pass


def test_invert_column_tags() -> None:
    column_tags = {
        'id': TyframeColumnTags('join_key'),
        'price': TyframeColumnTags(['unit_price', 'total_price']),
        'name': TyframeColumnTags(),
    }

    assert invert_column_tags(column_tags) == {
        'join_key': ['id'],
        'unit_price': ['price'],
        'total_price': ['price'],
    }


def test_invert_column_tags_multiple_columns_with_same_tag() -> None:
    column_tags = {
        'key_a': TyframeColumnTags('map_key'),
        'key_b': TyframeColumnTags('map_key'),
    }

    assert invert_column_tags(column_tags) == {'map_key': ['key_a', 'key_b']}


def test_invert_column_tags_empty() -> None:
    assert invert_column_tags({}) == {}


def test_invert_column_tags_with_extended_tag_type() -> None:
    column_tags = {
        'a': CustomColumnTags('custom'),
        'b': CustomColumnTags('map_key'),
    }

    result = invert_column_tags(column_tags)

    assert result == {'custom': ['a'], 'map_key': ['b']}
