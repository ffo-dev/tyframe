from pathlib import Path

from tests.test_classes.models import OneColModel, OtherExample, TwoColModel
from tyframe.base_df_model.base_df_model import BaseDfModel
from tyframe.code_gen.class_finder import find_child_classes


def test_find_child_classes_includes_indirect_descendants() -> None:
    file_path = Path(__file__).parents[1] / 'test_classes' / 'models.py'

    res = find_child_classes(file_path, BaseDfModel)
    assert sorted(res, key=lambda x: x.__name__) == sorted(
        [
            OneColModel,
            TwoColModel,
            OtherExample,
        ],
        key=lambda x: x.__name__,
    )
    assert all(el.__module__.startswith('tests.') for el in res)
