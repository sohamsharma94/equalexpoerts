from pathlib import Path

from equalexperts_dataeng_exercise.ingest import ingest_file
from equalexperts_dataeng_exercise.outliers import create_outlier_view


def test_outlier_view_matches_readme_example(tmp_path):
    database_path = tmp_path / "warehouse.db"
    sample_path = Path(__file__).parent / "test-resources" / "samples-votes.jsonl"

    ingest_file(sample_path, database_path)

    assert create_outlier_view(database_path) == [
        (2022, 0, 1),
        (2022, 1, 3),
        (2022, 2, 3),
        (2022, 5, 1),
        (2022, 6, 1),
        (2022, 8, 1),
    ]
