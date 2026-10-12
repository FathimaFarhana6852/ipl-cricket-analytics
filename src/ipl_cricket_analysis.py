from __future__ import annotations

import sqlite3
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "raw" / "ipl.db"
FIG_DIR = ROOT / "reports" / "figures"
REPORT_PATH = ROOT / "reports" / "analysis_report.md"


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_query(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    return pd.read_sql_query(query, conn)


def save_chase_win_rate_chart(df: pd.DataFrame) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    ax = df.plot(
        x="score_band",
        y="chase_win_rate_pct",
        kind="bar",
        color="#2f6fed",
        edgecolor="black",
        title="Chase win rate by first-innings total",
        figsize=(8, 5),
    )
    ax.set_xlabel("First-innings total")
    ax.set_ylabel("Chase win rate (%)")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", padding=3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "chase_win_rate.png", dpi=200)
    plt.close()


def save_toss_result_chart(df: pd.DataFrame) -> None:
    labels = ["Toss winner wins", "Toss winner loses"]
    values = [int(df.loc[0, "toss_winner_wins"]), int(df.loc[0, "toss_winner_losses"])]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(labels, values, color=["#1f77b4", "#d62728"], edgecolor="black")
    ax.set_title("Toss winner result vs match winner")
    ax.set_ylabel("Matches")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    for container in ax.containers:
        ax.bar_label(container, padding=3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "toss_result.png", dpi=200)
    plt.close()


def save_field_first_trend_chart(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["season_year"], df["field_first_pct"], marker="o", linewidth=2.5, color="#228B22")
    ax.set_title("Field-first decisions over time")
    ax.set_xlabel("Season")
    ax.set_ylabel("Field-first share (%)")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "field_first_trend.png", dpi=200)
    plt.close()


def build_insight_1(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        SELECT
            CASE
                WHEN first_innings_total < 140 THEN '<140'
                WHEN first_innings_total < 160 THEN '140-159'
                WHEN first_innings_total < 180 THEN '160-179'
                WHEN first_innings_total < 200 THEN '180-199'
                ELSE '200+'
            END AS score_band,
            COUNT(*) AS total_matches,
            ROUND(
                100.0 * SUM(CASE WHEN match_winner != innings1_batting_team THEN 1 ELSE 0 END) / COUNT(*),
                1
            ) AS chase_win_rate_pct
        FROM v_match_totals
        WHERE result = 'win' AND first_innings_total IS NOT NULL
        GROUP BY score_band
        ORDER BY CASE score_band
            WHEN '<140' THEN 1
            WHEN '140-159' THEN 2
            WHEN '160-179' THEN 3
            WHEN '180-199' THEN 4
            WHEN '200+' THEN 5
            ELSE 6
        END
    """
    return fetch_query(conn, query)


def build_insight_2(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        SELECT
            COUNT(*) AS total_matches,
            SUM(CASE WHEN toss_winner = match_winner THEN 1 ELSE 0 END) AS toss_winner_wins,
            SUM(CASE WHEN toss_winner != match_winner THEN 1 ELSE 0 END) AS toss_winner_losses
        FROM matches_clean
        WHERE result = 'win'
    """
    return fetch_query(conn, query)


def build_insight_3(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        SELECT
            CAST(season_year AS INTEGER) AS season_year,
            ROUND(
                100.0 * SUM(CASE WHEN LOWER(toss_decision) = 'field' THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS field_first_pct
        FROM matches_clean
        WHERE result = 'win'
        GROUP BY season_year
        ORDER BY season_year
    """
    return fetch_query(conn, query)


def render_report(insight_1: pd.DataFrame, insight_2: pd.DataFrame, insight_3: pd.DataFrame) -> None:
    toss_win_rate = round(100.0 * insight_2.loc[0, "toss_winner_wins"] / insight_2.loc[0, "total_matches"], 2)
    low_band = insight_1.loc[insight_1["score_band"] == "<140"].iloc[0]
    high_band = insight_1.loc[insight_1["score_band"] == "200+"].iloc[0]

    report = f"""# IPL Analysis Report
This report presents key business insights from the cleaned IPL dataset.

## Insight 1 — First-Innings Total and Chase Success
The analysis shows that the chase win rate decreases as the first-innings score increases, falling from **{low_band['chase_win_rate_pct']}% for scores below 140 (n={int(low_band['total_matches'])})** to **{high_band['chase_win_rate_pct']}% for scores of 200 or more (n={int(high_band['total_matches'])})** across **{int(insight_2.loc[0, 'total_matches'])} decisive matches**. This suggests that teams batting first can use higher first-innings totals to put greater pressure on the chasing team, with approximately **175 runs as a useful target to aim for**. However, the analysis does not consider factors such as **pitch conditions, player fitness, or injuries**, which may also affect match outcomes.
![Chase Win Rate](figures/chase_win_rate.png)

## Insight 2 — Toss Result and Match Success
The analysis shows that the **toss winner also won the match in {int(insight_2.loc[0, 'toss_winner_wins'])} out of {int(insight_2.loc[0, 'total_matches'])} decisive matches ({toss_win_rate}%)**, while the toss winner did not win in {int(insight_2.loc[0, 'toss_winner_losses'])} matches. This suggests that **winning the toss alone does not show a strong advantage in determining the final match result**, since the outcomes are nearly evenly split. Therefore, teams should **not rely on the toss result alone when making match strategies and should also consider factors such as batting performance, bowling performance, and match conditions**.
![Toss Result](figures/toss_result.png)

## Insight 3 — Field-First Decisions Over Time
The analysis shows that the preference for **fielding first after winning the toss increased over time**. Field-first decisions were **{float(insight_3.loc[insight_3['season_year'] == 2008, 'field_first_pct'].iat[0]):.2f}% in 2008**, **{float(insight_3.loc[insight_3['season_year'] == 2009, 'field_first_pct'].iat[0]):.2f}% in 2009**, and **{float(insight_3.loc[insight_3['season_year'] == 2010, 'field_first_pct'].iat[0]):.2f}% in 2010**, while they exceeded **80% in each season from 2016 to 2019**. This indicates a clear shift in team strategy toward choosing to chase during that period. Therefore, teams should **consider the increasing preference for chasing when planning toss strategy, while also evaluating season and match conditions rather than assuming that fielding first is always the better option**.
![Field-First Trend](figures/field_first_trend.png)
"""

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    conn = connect_db()
    try:
        chase_df = build_insight_1(conn)
        toss_df = build_insight_2(conn)
        field_df = build_insight_3(conn)

        save_chase_win_rate_chart(chase_df)
        save_toss_result_chart(toss_df)
        save_field_first_trend_chart(field_df)
        render_report(chase_df, toss_df, field_df)
        print("Analysis complete. Files saved to reports/.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
