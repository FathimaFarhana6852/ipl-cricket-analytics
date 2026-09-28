-- 03_venue_cleaning.sql
-- Standardize venue names

DROP VIEW IF EXISTS v_matches_clean;

CREATE VIEW v_matches_clean AS
SELECT
    *,
    CASE
        WHEN venue_comma_clean = 'M.Chinnaswamy Stadium'
        THEN 'M Chinnaswamy Stadium'
        ELSE venue_comma_clean
    END AS venue_clean
FROM (
    SELECT
        *,
        TRIM(
            SUBSTR(
                venue,
                1,
                CASE
                    WHEN INSTR(venue, ',') > 0
                    THEN INSTR(venue, ',') - 1
                    ELSE LENGTH(venue)
                END
            )
        ) AS venue_comma_clean
    FROM matches
);