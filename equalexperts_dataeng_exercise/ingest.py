import sys
from pathlib import Path

from equalexperts_dataeng_exercise.db import connect


def ingest_file(data_path: str | Path, database_path: str | Path = "warehouse.db") -> None:
    """Upsert the JSONL vote records from one input file into the warehouse."""
    path = Path(data_path)
    if not path.is_file():
        raise FileNotFoundError(f"Vote data file does not exist: {path}")

    connection = connect(database_path)
    try:
        connection.execute("BEGIN TRANSACTION")
        connection.execute(
            """
			CREATE TABLE IF NOT EXISTS blog_analysis.votes (
				id BIGINT PRIMARY KEY,
				post_id BIGINT NOT NULL,
				vote_type_id INTEGER NOT NULL,
				creation_date TIMESTAMP NOT NULL
			)
			"""
        )
        connection.execute(
            """
			CREATE OR REPLACE TEMP TABLE staged_votes AS
			SELECT
				CAST(Id AS BIGINT) AS id,
				CAST(PostId AS BIGINT) AS post_id,
				CAST(VoteTypeId AS INTEGER) AS vote_type_id,
				CAST(CreationDate AS TIMESTAMP) AS creation_date
			FROM read_json_auto(?, format = 'newline_delimited')
			QUALIFY ROW_NUMBER() OVER (
				PARTITION BY CAST(Id AS BIGINT)
				ORDER BY CAST(CreationDate AS TIMESTAMP) DESC,
				CAST(PostId AS BIGINT) DESC,
				CAST(VoteTypeId AS INTEGER) DESC
			) = 1
			""",
            [str(path.resolve())],
        )
        connection.execute(
            """
			MERGE INTO blog_analysis.votes AS target
			USING staged_votes AS source
				ON target.id = source.id
			WHEN MATCHED THEN UPDATE SET
				post_id = source.post_id,
				vote_type_id = source.vote_type_id,
				creation_date = source.creation_date
			WHEN NOT MATCHED THEN INSERT
				(id, post_id, vote_type_id, creation_date)
				VALUES (source.id, source.post_id, source.vote_type_id, source.creation_date)
			"""
        )
        connection.execute("COMMIT")
    except Exception:
        connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m equalexperts_dataeng_exercise.ingest <votes.jsonl>")
    ingest_file(sys.argv[1])
