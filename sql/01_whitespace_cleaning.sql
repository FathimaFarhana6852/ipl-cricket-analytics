-- 01_whitespace_cleaning.sql
-- Clean whitespace-only values in bowler_type and field_pos

DROP VIEW IF EXISTS v_deliveries_clean;

CREATE VIEW v_deliveries_clean AS
SELECT
    *,
    NULLIF(TRIM(bowler_type), '') AS bowler_type_clean
FROM deliveries;

DROP VIEW IF EXISTS v_players_clean;

CREATE VIEW v_players_clean AS
SELECT
    *,
    NULLIF(TRIM(field_pos), '') AS field_pos_clean
FROM players;