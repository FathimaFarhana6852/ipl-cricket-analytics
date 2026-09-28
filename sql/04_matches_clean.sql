-- 04_matches_clean.sql
-- Build the final cleaned matches table

DROP TABLE IF EXISTS matches_clean;

CREATE TABLE matches_clean AS

WITH ranked_venues AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY venue
            ORDER BY venue_id
        ) AS rn
    FROM venues
),
dedup_venues AS (
    SELECT *
    FROM ranked_venues
    WHERE rn = 1
)
SELECT
    m.*,
    COALESCE(v.city, m.city, 'UNKNOWN') AS city_clean,
    CAST(SUBSTR(m.season, 1, 4) AS INTEGER) AS season_year
FROM v_matches_clean m
LEFT JOIN dedup_venues v
    ON m.venue = v.venue;