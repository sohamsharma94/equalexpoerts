from equalexperts_dataeng_exercise.db import connect

OUTLIER_VIEW_SQL = """
CREATE OR REPLACE VIEW blog_analysis.outlier_weeks AS
WITH weekly_votes AS (
	SELECT
		YEAR(creation_date) AS year,
		CAST(FLOOR((DAYOFYEAR(creation_date) - 1) / 7) AS INTEGER) AS week_number,
		COUNT(*) AS vote_count
	FROM blog_analysis.votes
	GROUP BY year, week_number
), weekly_average AS (
	SELECT AVG(vote_count) AS average_vote_count
	FROM weekly_votes
)
SELECT
	weekly_votes.year AS "Year",
	weekly_votes.week_number AS "WeekNumber",
	weekly_votes.vote_count AS "VoteCount"
FROM weekly_votes
CROSS JOIN weekly_average
WHERE ABS(1 - weekly_votes.vote_count / weekly_average.average_vote_count) > 0.2
ORDER BY weekly_votes.year, weekly_votes.week_number
"""


def create_outlier_view(database_path: str = "warehouse.db") -> list[tuple[int, int, int]]:
    """Recreate the outlier view and return its rows in chronological order."""
    connection = connect(database_path)
    try:
        connection.execute(OUTLIER_VIEW_SQL)
        return connection.execute("SELECT * FROM blog_analysis.outlier_weeks").fetchall()
    finally:
        connection.close()


if __name__ == "__main__":
    rows = create_outlier_view()
    print("Year | WeekNumber | VoteCount")
    for row in rows:
        print(" | ".join(map(str, row)))
