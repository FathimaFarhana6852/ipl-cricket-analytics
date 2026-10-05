# IPL Analysis Report
This report presents key business insights from the cleaned IPL dataset.
## Insight 1 — First-Innings Total and Chase Success
The analysis shows that the chase win rate decreases as the first-innings score increases, falling from **82.6% for scores below 140 (n=219)** to **23.2% for scores of 200 or more (n=198)** across **1,187 decisive matches**. This suggests that teams batting first can use higher first-innings totals to put greater pressure on the chasing team, with approximately **175 runs as a useful target to aim for**. However, the analysis does not consider factors such as **pitch conditions, player fitness, or injuries**, which may also affect match outcomes. As a validation check, the **1,187 decisive matches identified in SQL were cross-checked in Excel, which also returned 1,187 matches**.
![Chase Win Rate](figures/chase_win_rate.png)
## Insight 2 — Toss Result and Match Success
The analysis shows that the **toss winner also won the match in 613 out of 1,187 decisive matches (51.64%)**, while the toss winner did not win in 574 matches. This suggests that **winning the toss alone does not show a strong advantage in determining the final match result**, since the outcomes are nearly evenly split. Therefore, teams should **not rely on the toss result alone when making match strategies and should also consider factors such as batting performance, bowling performance, and match conditions**.
![Toss Result](figures/toss_result.png)
## Insight 3 — Field-First Decisions Over Time
The analysis shows that the preference for **fielding first after winning the toss increased over time**. Field-first decisions were **55.17% in 2008, 38.60% in 2009, and 35.00% in 2010**, while they exceeded **80% in each season from 2016 to 2019**. This indicates a clear shift in team strategy toward choosing to chase during that period. Therefore, teams should **consider the increasing preference for chasing when planning toss strategy, while also evaluating season and match conditions rather than assuming that fielding first is always the better option**.
![Field-First Trend](figures/field_first_trend.png)
