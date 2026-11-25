from typing import TYPE_CHECKING

from tyframe.tagging.column_tags import TyframeColumnTags

if TYPE_CHECKING:
    from tyframe.tagging.column_tags import TyframeTag


def test_tyframe_column_tags_init() -> None:
    assert TyframeColumnTags() == []
    assert TyframeColumnTags(None) == []
    assert TyframeColumnTags('map_key') == ['map_key']
    assert TyframeColumnTags('join_value') == ['join_value']
    assert TyframeColumnTags(['join_key', 'map_value']) == ['join_key', 'map_value']
    assert TyframeColumnTags(('map_key', 'join_key')) == ['map_key', 'join_key']
    source: list[TyframeTag] = ['map_value']
    assert TyframeColumnTags(iter(source)) == ['map_value']


def test_add_tag_appends_new_tag() -> None:
    tags = TyframeColumnTags('map_key')
    tags.add_tag('join_value')
    assert tags == ['map_key', 'join_value']


def test_add_tag_ignores_duplicate() -> None:
    tags = TyframeColumnTags(['map_key'])
    tags.add_tag('map_key')
    assert tags == ['map_key']


def test_remove_tag_removes_existing_tag() -> None:
    tags = TyframeColumnTags(['map_key', 'join_value'])
    tags.remove_tag('map_key')
    assert tags == ['join_value']


def test_remove_tag_ignores_missing_tag() -> None:
    tags = TyframeColumnTags(['map_key'])
    tags.remove_tag('join_value')
    assert tags == ['map_key']
