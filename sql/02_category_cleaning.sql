-- 02_category_cleaning.sql
-- Standardize category variants identified during profiling

DROP VIEW IF EXISTS v_deliveries_category_clean;

CREATE VIEW v_deliveries_category_clean AS
SELECT
    *,
    CASE
        WHEN NULLIF(TRIM(bowler_type), '') = 'Right arm Fast Medium'
        THEN 'Right arm Fast medium'
        ELSE NULLIF(TRIM(bowler_type), '')
    END AS bowler_type_clean
FROM deliveries;

DROP VIEW IF EXISTS v_teams_clean;

CREATE VIEW v_teams_clean AS
SELECT
    *,
    CASE
        WHEN team_name = 'Rising Pune Supergiants'
        THEN 'Rising Pune Supergiant'
        ELSE team_name
    END AS team_name_clean
FROM teams;