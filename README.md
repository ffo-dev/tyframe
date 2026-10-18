# tyframe

basedpyright .
pytest --cov=src/tyframe src/tests/ --cov-report=term-missing


tyframe generate-typed-wrapper src/tests/test_classes src/tests/generated_models/pandas tyframe_config.yml pandas Pd
tyframe generate-typed-wrapper src/tests/test_classes src/tests/generated_models/polars tyframe_config.yml polars Pl
tyframe generate-typed-wrapper src/tests/test_classes src/tests/generated_models/lazy_polars tyframe_config.yml polars Lpl
uv run ruff check --fix --config ruff.toml 