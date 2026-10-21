import json

import duckdb

from equalexperts_dataeng_exercise.ingest import ingest_file


def write_votes(path, records):
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def vote(vote_id, post_id, vote_type_id, date):
    return {
        "Id": str(vote_id),
        "PostId": str(post_id),
        "VoteTypeId": str(vote_type_id),
        "CreationDate": date,
    }


def test_ingestion_is_incremental_and_updates_existing_ids(tmp_path):
    database_path = tmp_path / "warehouse.db"
    first_batch = tmp_path / "first.jsonl"
    second_batch = tmp_path / "second.jsonl"
    write_votes(first_batch, [vote(1, 10, 2, "2022-01-02T00:00:00.000")])
    write_votes(
        second_batch,
        [
            vote(1, 11, 3, "2022-01-03T00:00:00.000"),
            vote(2, 12, 2, "2022-01-09T00:00:00.000"),
        ],
    )

    ingest_file(first_batch, database_path)
    ingest_file(second_batch, database_path)
    ingest_file(second_batch, database_path)

    with duckdb.connect(str(database_path), read_only=True) as connection:
        records = connection.execute("SELECT id, post_id, vote_type_id FROM blog_analysis.votes ORDER BY id").fetchall()
    assert records == [(1, 11, 3), (2, 12, 2)]


def test_ingestion_deduplicates_repeated_ids_within_a_file(tmp_path):
    database_path = tmp_path / "warehouse.db"
    input_path = tmp_path / "votes.jsonl"
    write_votes(
        input_path,
        [
            vote(1, 10, 2, "2022-01-02T00:00:00.000"),
            vote(1, 11, 2, "2022-01-03T00:00:00.000"),
        ],
    )

    ingest_file(input_path, database_path)

    with duckdb.connect(str(database_path), read_only=True) as connection:
        records = connection.execute("SELECT id, post_id FROM blog_analysis.votes").fetchall()
    assert records == [(1, 11)]
