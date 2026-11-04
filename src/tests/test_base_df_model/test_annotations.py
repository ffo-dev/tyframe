from tyframe.base_df_model import BaseDfModel


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
