from pathlib import Path

import duckdb


def connect(database_path: str | Path = "warehouse.db") -> duckdb.DuckDBPyConnection:
    """Open the local DuckDB warehouse and ensure its application schema exists."""
    connection = duckdb.connect(str(database_path))
    connection.execute("CREATE SCHEMA IF NOT EXISTS blog_analysis")
    return connection
