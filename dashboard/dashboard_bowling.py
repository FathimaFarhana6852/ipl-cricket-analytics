import os
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import streamlit as st
 
st.set_page_config(page_title="IPL Bowling Dashboard", page_icon="🏏",
                   layout="wide", initial_sidebar_state="expanded")
 
PHASES = ["Powerplay", "Middle Overs", "Death Overs"]
 
CREDITED = ["bowled", "caught", "caughtandbowled", "lbw", "stumped", "hitwicket"]
 
COUNT_RUN_OUTS_IN_CHARTS = True
 
MIN_BALLS_FOR_TEST = 200      
 
 
def find_db():
    """Looks for ipl.db in the usual places (relative paths only)."""
    here = os.path.dirname(os.path.abspath(__file__))
    options = [os.path.join(here, "..", "data", "raw", "ipl.db"),
               os.path.join(here, "..", "data", "ipl.db"),
               os.path.join(here, "data", "raw", "ipl.db"),
               os.path.join(here, "data", "ipl.db"),
               os.path.join(here, "ipl.db")]
    for path in options:
        if os.path.exists(path):
            return path
    return None
 
 
def bowling_group(x):
    """Spin / Pace rule from your notebook (spin words are checked first)."""
    x = str(x).lower()
    if any(w in x for w in ["spin", "legbreak", "offbreak", "orthodox"]):
        return "Spin"
    if "fast" in x or "medium" in x:
        return "Pace"
    return None
 
 
@st.cache_data(ttl=600)
def load_data():
    path = find_db()
    if path is None:
        return None
    con = sqlite3.connect(path)
    df = pd.read_sql_query("""
        SELECT d.match_id, d.bowler, d.bowler_type_clean, d.over_number,
               d.total_runs, d.bye_runs, d.leg_bye_runs, d.penalty_runs,
               d.is_wide_ball, d.is_no_ball, d.is_wicket, d.wicket_kind,
               d.batting_team AS opponent,
               m.season_year AS season, m.venue_clean AS venue
        FROM v_deliveries_category_clean d
        JOIN matches_clean m ON d.match_id = m.match_id
        WHERE d.is_super_over = 0
    """, con)
    con.close()
 
    df["bowling_style"] = df["bowler_type_clean"].fillna("Unknown")
    df["bowling_group"] = df["bowler_type_clean"].apply(bowling_group)
    df["phase"] = pd.cut(df["over_number"], bins=[-1, 5, 14, 19], labels=PHASES).astype(str)
 
    df["runs_conceded"] = (df["total_runs"] - df["bye_runs"].fillna(0)
                           - df["leg_bye_runs"].fillna(0) - df["penalty_runs"].fillna(0))
   
    df["legal_ball"] = ((df["is_wide_ball"] == 0) & (df["is_no_ball"] == 0)).astype(int)
    
    df["dot_ball"] = ((df["legal_ball"] == 1) & (df["total_runs"] == 0)).astype(int)
 
    kind = (df["wicket_kind"].fillna("").str.strip().str.lower()
            .str.replace(" ", "", regex=False).str.replace("-", "", regex=False))
    df["credited_wicket"] = ((df["is_wicket"] == 1) & kind.isin(CREDITED)).astype(int)
    df["wicket"] = df["is_wicket"] if COUNT_RUN_OUTS_IN_CHARTS else df["credited_wicket"]
 
    df["dismissal"] = kind.map({"bowled": "Bowled", "caught": "Caught",
                                "caughtandbowled": "Caught", "lbw": "LBW",
                                "stumped": "Stumped", "hitwicket": "Hit Wicket"})
    df.loc[df["credited_wicket"] == 0, "dismissal"] = None
    return df
 
 
def summarise(d, by):
    """Group the data. Economy rate = runs conceded x 6 / legal balls"""
    t = d.groupby(by, observed=True).agg(
        runs=("runs_conceded", "sum"), balls=("legal_ball", "sum"),
        wickets=("wicket", "sum")).reset_index()
    t["economy"] = (6 * t["runs"] / t["balls"].replace(0, np.nan)).round(2)
    return t
 
 
def order_phases(t):
    t = t[t["phase"].isin(PHASES)].copy()
    t["phase"] = pd.Categorical(t["phase"], categories=PHASES, ordered=True)
    return t.sort_values("phase")
 
 
def season_axis(t):
    """Season as text so the chart shows 2008, 2009 ... in order."""
    t = t.sort_values("season").copy()
    t["season"] = t["season"].astype(int).astype(str)
    return t
 
 
df = load_data()
if df is None:
    st.error("Could not find ipl.db. Keep it in data/raw/ipl.db (one folder above this file) "
             "or in a 'data' folder next to it.")
    st.stop()
 
st.title("🏏 IPL Bowling Analytics Dashboard")
st.caption("IPL bowling performance and player statistics analysis")
 
with st.sidebar:
    st.header("🔍 Filters")
    season = st.selectbox("Season", ["All"] + sorted(df["season"].unique().tolist()))
 
    style_options = sorted(df["bowling_style"].unique())
    styles = st.multiselect("Bowling Style", options=style_options, default=style_options)
 
    phases = st.multiselect("Bowling Phase", options=PHASES, default=PHASES)
 
    min_balls = st.slider("Minimum Balls Bowled", 0, 500, 0, step=10)
    min_wkts = st.slider("Minimum Wickets", 0, 50, 0)
 
    name = st.text_input("Bowler Name", placeholder="🔍 Search bowler...")
 
    opp_options = sorted(df["opponent"].dropna().unique())
    opps = st.multiselect("Opponent Team", options=opp_options, default=opp_options)
 
    if st.button("🔄️ Refresh data"):
        st.cache_data.clear()
        st.rerun()
 
filtered = df[df["bowling_style"].isin(styles)
              & df["phase"].isin(phases)
              & df["opponent"].isin(opps)]
if season != "All":
    filtered = filtered[filtered["season"] == season]
league_df = filtered         
if name:
    filtered = filtered[filtered["bowler"].str.contains(name, case=False, regex=False)]
 
per_bowler = summarise(filtered, "bowler")
eligible = per_bowler[(per_bowler["balls"] >= min_balls)
                      & (per_bowler["wickets"] >= min_wkts)]["bowler"]
filtered = filtered[filtered["bowler"].isin(eligible)]
 
st.sidebar.divider()
st.sidebar.download_button("📥 Download filtered data",
                           data=filtered.to_csv(index=False).encode("utf-8"),
                           file_name="bowling_filtered.csv", mime="text/csv")
 
if filtered.empty:
    st.warning("No data for the selected filters. Try lowering the minimum balls / wickets.")
    st.stop()
 
tab1, tab2 = st.tabs(["📋 Overview", "🎯 Bowler"])

with tab1:
    b = filtered[filtered["bowler_type_clean"].notna()].groupby(
        ["bowler", "bowler_type_clean"]).agg(
        runs=("runs_conceded", "sum"), balls=("legal_ball", "sum")).reset_index()
    b["economy"] = 6 * b["runs"] / b["balls"].replace(0, np.nan)
    b = b[b["balls"] >= MIN_BALLS_FOR_TEST].copy()
    b["group"] = b["bowler_type_clean"].apply(bowling_group)
    spin = b.loc[b["group"] == "Spin", "economy"].dropna()
    pace = b.loc[b["group"] == "Pace", "economy"].dropna()
 
    if len(spin) > 1 and len(pace) > 1:
        p_value = stats.ttest_ind(spin, pace, equal_var=False).pvalue
        pooled_sd = np.sqrt(((len(spin) - 1) * spin.var(ddof=1)
                             + (len(pace) - 1) * pace.var(ddof=1))
                            / (len(spin) + len(pace) - 2))
        cohens_d = (pace.mean() - spin.mean()) / pooled_sd
        pe_text = f"{p_value:.2e} | {cohens_d:.2f}"
        verdict = ("statistically significant" if p_value < 0.05
                   else "not statistically significant")
        note = (f"Spin vs Pace is {verdict}. Spin mean economy {spin.mean():.2f} "
                f"({len(spin)} bowlers) vs Pace {pace.mean():.2f} ({len(pace)} bowlers), "
                f"bowlers with at least {MIN_BALLS_FOR_TEST} legal balls.")
    else:
        pe_text = "n/a"
        note = (f"Not enough spin and pace bowlers with {MIN_BALLS_FOR_TEST}+ legal balls "
                "in the current filters.")
 
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Bowlers", filtered["bowler"].nunique())
    c2.metric("Total Bowler-Credited Wickets", int(filtered["credited_wicket"].sum()))
    c3.metric("Spin vs Pace (p-value | effect size)", pe_text)
    st.caption(note)
 
    with st.expander("ℹ️ How are these values calculated?"):
        st.markdown(f"""
- **Legal ball** = not a wide and not a no-ball.
- **Runs conceded** = total runs − bye runs − leg-bye runs − penalty runs.
- **Economy rate** = runs conceded × 6 ÷ legal balls.
- **Phases** = Powerplay (overs 1-6), Middle Overs (7-15), Death Overs (16-20). Super overs are excluded.
- **Bowler-credited wickets** = bowled, caught, caught & bowled, lbw, stumped, hit wicket (run outs are not credited to the bowler).
- **Wickets in charts** = {"all dismissals (run outs included)" if COUNT_RUN_OUTS_IN_CHARTS else "bowler-credited wickets only"}.
- **Dot-ball share** = dot balls ÷ legal balls × 100 (dot ball = legal ball with 0 total runs).
- **Spin vs Pace p-value** = Welch's t-test on each bowler's economy rate (bowlers with ≥ {MIN_BALLS_FOR_TEST} legal balls).
- **Effect size (Cohen's d)** = (mean pace economy − mean spin economy) ÷ pooled SD. Positive = spin is cheaper. 0.2 small, 0.5 medium, 0.8 large.
        """)
 
    col1, col2 = st.columns(2)
    with col1:
        g = order_phases(summarise(filtered[filtered["bowling_group"].notna()],
                                   ["phase", "bowling_group"]))
        league = order_phases(summarise(filtered, "phase"))
        fig = px.bar(g, x="phase", y="economy", color="bowling_group", barmode="group",
                     text="economy", category_orders={"phase": PHASES,
                                                      "bowling_group": ["Spin", "Pace"]},
                     title="Spin v/s Pace: Economy Rate Across Bowling Phases",
                     labels={"phase": "Bowling Phase", "economy": "Economy Rate",
                             "bowling_group": "Bowling Group"})
        fig.add_trace(go.Scatter(x=league["phase"].astype(str), y=league["economy"],
                                 mode="markers", name="League Economy",
                                 marker=dict(symbol="line-ew", size=45, color="black",
                                             line=dict(width=3, color="black"))))
        st.plotly_chart(fig)
 
    with col2:
        s = filtered[filtered["bowler_type_clean"].notna()].groupby("bowler_type_clean").agg(
            runs=("runs_conceded", "sum"), balls=("legal_ball", "sum"),
            bowlers=("bowler", "nunique")).reset_index()
        s = s[s["balls"] > 0].copy()
        s["economy"] = (6 * s["runs"] / s["balls"]).round(2)
        s = s.sort_values("economy").head(5)
        s["label"] = s["economy"].astype(str) + " (Bowlers: " + s["bowlers"].astype(str) + ")"
        fig = px.bar(s, x="economy", y="bowler_type_clean", orientation="h", text="label",
                     title="Bowling Styles Ranked by Economy (Top 5)",
                     labels={"bowler_type_clean": "Bowling Style", "economy": "Economy Rate"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig)
 
    col3, col4 = st.columns(2)
    with col3:
        ph = order_phases(summarise(filtered, "phase"))
        fig = px.bar(ph, x="phase", y="wickets", text="wickets",
                     title="Wickets by Innings Phase",
                     labels={"phase": "Innings Phase", "wickets": "No. of Wickets"})
        st.plotly_chart(fig)
 
    with col4:
        tr = season_axis(summarise(filtered, "season"))
        fig = px.line(tr, x="season", y="wickets", markers=True,
                      title="Wicket Trend Across Season",
                      labels={"season": "Season", "wickets": "No. of Wickets"})
        st.plotly_chart(fig)
 
    st.subheader("Bowler Dismissal Summary Table")
    dis = (filtered.dropna(subset=["dismissal"]).groupby("dismissal").size()
           .reset_index(name="No. of Wickets")
           .sort_values("No. of Wickets", ascending=False))
    dis["Percentage of Total Wickets"] = (dis["No. of Wickets"] / dis["No. of Wickets"].sum()
                                          * 100).round(1).astype(str) + "%"
    dis = dis.rename(columns={"dismissal": "Dismissal Type"})
    st.dataframe(dis, hide_index=True)
 

with tab2:
    scope = filtered      
 
    balls = scope["legal_ball"].sum()
    economy = 6 * scope["runs_conceded"].sum() / balls if balls else 0
    dot_share = scope["dot_ball"].sum() / balls * 100 if balls else 0
 
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Wickets", int(scope["wicket"].sum()))
    c2.metric("Economy Rate", f"{economy:.2f}")
    c3.metric("Dot-ball Share", f"{dot_share:.1f}%")
 
    col1, col2 = st.columns(2)
    
    with col1:
        se = season_axis(summarise(scope, "season"))
        lg = season_axis(summarise(league_df, "season"))
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=se["season"], y=se["economy"], mode="lines+markers",
                                 name="Selected bowlers"))
        fig.add_trace(go.Scatter(x=lg["season"], y=lg["economy"], mode="lines+markers",
                                 name="League Economy", line=dict(dash="dash")))
        fig.update_layout(title="Economy by Season", xaxis_title="Season",
                          yaxis_title="Economy Rate")
        st.plotly_chart(fig)
 
    with col2:
        pe = order_phases(summarise(scope, "phase"))
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_bar(x=pe["phase"].astype(str), y=pe["wickets"], name="Wickets",
                    offsetgroup=0, text=pe["wickets"], secondary_y=False)
        fig.add_bar(x=pe["phase"].astype(str), y=pe["economy"], name="Economy Rate",
                    offsetgroup=1, text=pe["economy"], secondary_y=True)
        fig.update_layout(title="Wickets and Economy by Innings Phase", barmode="group",
                          xaxis_title="Innings Phase")
        fig.update_yaxes(title_text="Wickets", secondary_y=False)
        fig.update_yaxes(title_text="Economy Rate", secondary_y=True)
        st.plotly_chart(fig)
 
   
    op = summarise(scope, "opponent").sort_values("economy")
    op["label"] = op["economy"].astype(str) + " (Balls: " + op["balls"].astype(str) + ")"
    fig = px.bar(op, x="economy", y="opponent", orientation="h", text="label",
                 title="Economy Rate Against Opponent Team",
                 labels={"opponent": "Opponent Team", "economy": "Economy Rate"})
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
 
   
    st.subheader("Bowler Performance by Venue")
    ven = scope.groupby("venue").agg(
        Matches=("match_id", "nunique"), Balls_Bowled=("legal_ball", "sum"),
        Wickets=("wicket", "sum"), runs=("runs_conceded", "sum")).reset_index()
    ven["Economy Rate"] = (6 * ven["runs"] / ven["Balls_Bowled"].replace(0, np.nan)).round(2)
    ven = ven.drop(columns="runs").rename(columns={"venue": "Venue",
                                                   "Balls_Bowled": "Balls Bowled"})
    st.dataframe(ven.sort_values("Wickets", ascending=False), hide_index=True)
 
    pw = order_phases(summarise(scope, "phase"))
    fig = px.pie(pw, names="phase", values="wickets", title="Wickets by Bowling Phase",
                 category_orders={"phase": PHASES})
    fig.update_traces(textinfo="label+value+percent")
    st.plotly_chart(fig)
 
st.markdown("---")
st.caption(f"Showing {len(filtered):,} deliveries · "
           f"{int(filtered['season'].min())}-{int(filtered['season'].max())} · "
           f"{filtered['bowler'].nunique()} bowlers")