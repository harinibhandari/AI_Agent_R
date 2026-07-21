import importlib


def test_duckdb_module_import():
    module = importlib.import_module("app.database.duckdb_manager")
    assert module is not None