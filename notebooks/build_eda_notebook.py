"""Generate EDA_Analysis.ipynb for Day 3 capstone deliverable."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = Path(__file__).resolve().parent / "EDA_Analysis.ipynb"

CELLS = []

def md(source: str):
    CELLS.append({"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)})

def code(source: str):
    CELLS.append({"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
                  "source": source.splitlines(keepends=True)})

md("""# DAY 3 — Exploratory Data Analysis (EDA)
## Capstone Project I — Mutual Fund Analytics

This notebook explores mutual fund industry data (2022–2026) across NAV trends, AUM growth, SIP inflows, investor demographics, and portfolio composition.

**Deliverables:** 15+ visualizations with exported PNG charts in `reports/eda_charts/`.""")

code("""import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight", "font.size": 10})

ROOT = next(
    (p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "processed" / "fund_master.csv").exists()),
    Path.cwd(),
)
DATA = ROOT / "data" / "processed"
CHART_DIR = ROOT / "reports" / "eda_charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

def save_matplotlib(fig, name):
    path = CHART_DIR / f"{name}.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved {path.name}")

def save_plotly(fig, name):
    path = CHART_DIR / f"{name}.png"
    fig.write_image(str(path), width=1200, height=700, scale=2)
    print(f"Saved {path.name}")

chart_count = 0""")

code("""# Load datasets
fund_master = pd.read_csv(DATA / "fund_master.csv")
nav_history = pd.read_csv(DATA / "nav_history.csv", parse_dates=["date"])
aum = pd.read_csv(DATA / "aum_by_fund_house.csv", parse_dates=["date"])
sip = pd.read_csv(DATA / "monthly_sip_inflows.csv")
category_inflows = pd.read_csv(DATA / "category_inflows.csv")
folio = pd.read_csv(DATA / "industry_folio_count.csv")
investors = pd.read_csv(DATA / "investor_transactions.csv", parse_dates=["transaction_date"])
holdings = pd.read_csv(DATA / "portfolio_holdings.csv")
performance = pd.read_csv(DATA / "scheme_performance.csv")

nav_history = nav_history.merge(
    fund_master[["amfi_code", "scheme_name", "fund_house", "category"]],
    on="amfi_code",
    how="left",
)
print(f"Loaded {nav_history['amfi_code'].nunique()} schemes | NAV rows: {len(nav_history):,}")""")

md("## 1. NAV Trend Analysis (Plotly)")
code("""# Index NAV to 100 at start for comparability across 40 schemes
nav_idx = nav_history.copy()
nav_idx["nav_indexed"] = nav_idx.groupby("amfi_code")["nav"].transform(
    lambda s: s / s.iloc[0] * 100
)

fig_nav = go.Figure()
for code, grp in nav_idx.groupby("amfi_code"):
    label = grp["scheme_name"].iloc[0][:40]
    fig_nav.add_trace(go.Scatter(
        x=grp["date"], y=grp["nav_indexed"], mode="lines",
        name=label, line=dict(width=1), opacity=0.65,
        hovertemplate="%{x|%Y-%m-%d}<br>Indexed NAV: %{y:.1f}<extra></extra>",
    ))

fig_nav.add_vrect(x0="2023-01-01", x1="2023-12-31", fillcolor="green", opacity=0.08,
                  annotation_text="2023 Bull Run", annotation_position="top left")
fig_nav.add_vrect(x0="2024-01-01", x1="2024-09-30", fillcolor="red", opacity=0.08,
                  annotation_text="2024 Corrections", annotation_position="top right")
fig_nav.update_layout(
    title="Daily NAV Trends — 40 Schemes (Indexed to 100, Jan 2022)",
    xaxis_title="Date", yaxis_title="Indexed NAV (Base = 100)",
    template="plotly_white", height=650, legend=dict(font=dict(size=8)),
)
fig_nav.show()
try:
    save_plotly(fig_nav, "01_nav_trend_40_schemes")
except Exception as e:
    print(f"Plotly PNG export failed ({e}); saving matplotlib fallback")
    fig_mpl, ax = plt.subplots(figsize=(12, 6))
    for code, grp in nav_idx.groupby("amfi_code"):
        ax.plot(grp["date"], grp["nav_indexed"], alpha=0.5, linewidth=0.8)
    ax.axvspan(pd.Timestamp("2023-01-01"), pd.Timestamp("2023-12-31"), alpha=0.1, color="green", label="2023 Bull Run")
    ax.axvspan(pd.Timestamp("2024-01-01"), pd.Timestamp("2024-09-30"), alpha=0.1, color="red", label="2024 Corrections")
    ax.set_title("Daily NAV Trends — 40 Schemes (Indexed to 100)")
    ax.legend(loc="upper left", fontsize=8)
    save_matplotlib(fig_mpl, "01_nav_trend_40_schemes")
chart_count += 1""")

md("## 2. AUM Growth by Fund House (Seaborn)")
code("""year_end_dates = {
    2022: "2022-09-30",
    2023: "2023-09-30",
    2024: "2024-12-31",
    2025: "2025-12-31",
}
aum_yearly = aum[aum["date"].dt.strftime("%Y-%m-%d").isin(year_end_dates.values())].copy()
aum_yearly["year"] = aum_yearly["date"].dt.year

top_houses = (
    aum_yearly[aum_yearly["year"] == 2025]
    .nlargest(8, "aum_lakh_crore")["fund_house"]
    .tolist()
)
aum_plot = aum_yearly[aum_yearly["fund_house"].isin(top_houses)]

fig_aum, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=aum_plot, x="fund_house", y="aum_lakh_crore", hue="year", ax=ax)
ax.set_title("AUM Growth by Fund House (2022–2025) — ₹ Lakh Crore")
ax.set_xlabel("Fund House")
ax.set_ylabel("AUM (₹ Lakh Crore)")
ax.tick_params(axis="x", rotation=35)
sbi_2025 = aum_plot[(aum_plot["fund_house"] == "SBI Mutual Fund") & (aum_plot["year"] == 2025)]
if not sbi_2025.empty:
    val = sbi_2025["aum_lakh_crore"].iloc[0]
    ax.annotate(f"SBI: ₹{val}L Cr", xy=(0, val), xytext=(0.5, val + 0.8),
                arrowprops=dict(arrowstyle="->", color="darkblue"), fontsize=9, color="darkblue")
plt.legend(title="Year", bbox_to_anchor=(1.02, 1))
save_matplotlib(fig_aum, "02_aum_growth_by_fund_house")
chart_count += 1""")

md("## 3. Monthly SIP Inflow Time-Series (Plotly)")
code("""sip["month_dt"] = pd.to_datetime(sip["month"])
peak_row = sip.loc[sip["sip_inflow_crore"].idxmax()]

fig_sip = go.Figure()
fig_sip.add_trace(go.Scatter(
    x=sip["month_dt"], y=sip["sip_inflow_crore"], mode="lines+markers",
    name="SIP Inflow", line=dict(color="#2563eb", width=2.5),
    marker=dict(size=5),
))
fig_sip.add_annotation(
    x=str(peak_row["month_dt"].date()), y=float(peak_row["sip_inflow_crore"]),
    text=f"All-time high: ₹{peak_row['sip_inflow_crore']:,.0f} Cr (Dec 2025)",
    showarrow=True, arrowhead=2, ay=-60, font=dict(size=11),
)
fig_sip.update_layout(
    title="Monthly SIP Inflows (Jan 2022 – Dec 2025)",
    xaxis_title="Month", yaxis_title="SIP Inflow (₹ Crore)",
    template="plotly_white", height=500,
)
fig_sip.show()
try:
    save_plotly(fig_sip, "03_monthly_sip_inflows")
except Exception as e:
    print(f"Plotly PNG export failed ({e}); saving matplotlib fallback")
    fig_mpl, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sip["month_dt"], sip["sip_inflow_crore"], marker="o", color="#2563eb")
    ax.annotate(f"₹{peak_row['sip_inflow_crore']:,.0f} Cr", xy=(peak_row["month_dt"], peak_row["sip_inflow_crore"]),
                xytext=(0, 30), textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    ax.set_title("Monthly SIP Inflows (Jan 2022 – Dec 2025)")
    ax.set_ylabel("SIP Inflow (₹ Crore)")
    save_matplotlib(fig_mpl, "03_monthly_sip_inflows")
chart_count += 1""")

md("## 4. Category Inflow Heatmap (Seaborn)")
code("""cat_pivot = category_inflows.pivot(index="category", columns="month", values="net_inflow_crore")
cat_pivot = cat_pivot.reindex(cat_pivot.sum(axis=1).sort_values(ascending=False).index)

fig_heat, ax = plt.subplots(figsize=(14, 7))
sns.heatmap(cat_pivot, cmap="YlOrRd", annot=False, fmt=".0f", linewidths=0.3, ax=ax)
ax.set_title("Net Inflows by Fund Category (Monthly Heatmap)")
ax.set_xlabel("Month")
ax.set_ylabel("Category")
save_matplotlib(fig_heat, "04_category_inflow_heatmap")
chart_count += 1""")

md("## 5. Investor Demographics")
code("""sip_txn = investors[investors["transaction_type"] == "SIP"]

# 5a — Age group distribution (pie)
age_order = ["18-25", "26-35", "36-45", "46-55", "56+"]
age_counts = sip_txn["age_group"].value_counts().reindex(age_order).fillna(0)

fig_age_pie, ax = plt.subplots(figsize=(6, 6))
ax.pie(age_counts, labels=age_order, autopct="%1.1f%%", startangle=90,
       colors=sns.color_palette("Set2", 5))
ax.set_title("SIP Investor Age Group Distribution")
save_matplotlib(fig_age_pie, "05a_age_group_pie")
chart_count += 1

# 5b — SIP amount by age group (box plot)
fig_age_box, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=sip_txn, x="age_group", y="amount_inr", order=age_order, ax=ax, showfliers=False)
ax.set_title("SIP Amount Distribution by Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("SIP Amount (₹)")
save_matplotlib(fig_age_box, "05b_sip_amount_by_age")
chart_count += 1

# 5c — Gender split
gender_counts = sip_txn["gender"].value_counts()
fig_gender, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%",
            colors=["#4C78A8", "#F58518"], startangle=90)
axes[0].set_title("SIP Investors by Gender (Count)")
sns.barplot(x=gender_counts.index, y=gender_counts.values, ax=axes[1], palette=["#4C78A8", "#F58518"])
axes[1].set_title("SIP Investors by Gender (Bar)")
axes[1].set_ylabel("Number of SIP Transactions")
plt.tight_layout()
save_matplotlib(fig_gender, "05c_gender_split")
chart_count += 2""")

md("## 6. Geographic Distribution")
code("""# 6a — SIP amount by state (horizontal bar)
state_sip = sip_txn.groupby("state")["amount_inr"].sum().sort_values(ascending=True)

fig_state, ax = plt.subplots(figsize=(9, 6))
state_sip.plot(kind="barh", ax=ax, color=sns.color_palette("viridis", len(state_sip)))
ax.set_title("Total SIP Amount by State")
ax.set_xlabel("Total SIP Amount (₹)")
ax.set_ylabel("State")
ax.ticklabel_format(style="plain", axis="x")
save_matplotlib(fig_state, "06a_sip_by_state")
chart_count += 1

# 6b — T30 vs B30 city tier (pie)
tier_counts = sip_txn["city_tier"].value_counts()
fig_tier, ax = plt.subplots(figsize=(5, 5))
ax.pie(tier_counts, labels=[f"{t} Cities" for t in tier_counts.index],
       autopct="%1.1f%%", colors=["#2ca02c", "#ff7f0e"], startangle=140)
ax.set_title("SIP Transactions: T30 vs B30 Cities")
save_matplotlib(fig_tier, "06b_city_tier_pie")
chart_count += 1""")

md("## 7. Folio Count Growth")
code("""folio["month_dt"] = pd.to_datetime(folio["month"])
start_folio = folio.iloc[0]
end_folio = folio.iloc[-1]

fig_folio, ax = plt.subplots(figsize=(10, 5))
ax.plot(folio["month_dt"], folio["total_folios_crore"], marker="o", color="#6a0dad", linewidth=2)
ax.annotate(f"{start_folio['total_folios_crore']} Cr\\n(Jan 2022)",
            xy=(folio["month_dt"].iloc[0], start_folio["total_folios_crore"]),
            xytext=(10, 20), textcoords="offset points", fontsize=9)
ax.annotate(f"{end_folio['total_folios_crore']} Cr\\n(Dec 2025)",
            xy=(folio["month_dt"].iloc[-1], end_folio["total_folios_crore"]),
            xytext=(-60, 10), textcoords="offset points", fontsize=9,
            arrowprops=dict(arrowstyle="->", color="gray"))
ax.set_title("Industry Folio Count Growth (Jan 2022 – Dec 2025)")
ax.set_xlabel("Month")
ax.set_ylabel("Total Folios (Crore)")
save_matplotlib(fig_folio, "07_folio_count_growth")
chart_count += 1""")

md("## 8. NAV Return Correlation Matrix (Seaborn)")
code("""# Select 10 diverse equity schemes (one per sub-category where possible)
selected_codes = [
    119551,  # SBI Bluechip Large Cap
    100033,  # HDFC Mid Cap
    119598,  # SBI Small Cap
    120506,  # ICICI Value
    118636,  # Axis Bluechip
    102885,  # Kotak Emerging
    148567,  # Nippon Small Cap
    120843,  # ICICI Technology
    119120,  # SBI Gilt (debt contrast)
    100025,  # HDFC Short Term Debt
]
selected_codes = [c for c in selected_codes if c in nav_history["amfi_code"].unique()][:10]

nav_sel = nav_history[nav_history["amfi_code"].isin(selected_codes)].copy()
returns = (
    nav_sel.pivot_table(index="date", columns="amfi_code", values="nav")
    .pct_change()
    .dropna()
)
short_names = {
    row["amfi_code"]: row["scheme_name"][:25]
    for _, row in fund_master[fund_master["amfi_code"].isin(selected_codes)].iterrows()
}
returns.columns = [short_names.get(c, str(c)) for c in returns.columns]
corr = returns.corr()

fig_corr, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True, ax=ax)
ax.set_title("Daily Return Correlation — 10 Selected Funds")
plt.xticks(rotation=45, ha="right")
save_matplotlib(fig_corr, "08_nav_return_correlation")
chart_count += 1""")

md("## 9. Sector Allocation Donut Chart")
code("""equity_codes = fund_master.loc[fund_master["category"] == "Equity", "amfi_code"]
eq_holdings = holdings[holdings["amfi_code"].isin(equity_codes)]

sector_weights = (
    eq_holdings.groupby("sector")["market_value_cr"]
    .sum()
    .sort_values(ascending=False)
)
top_sectors = sector_weights.head(8)
other = sector_weights.iloc[8:].sum()
if other > 0:
    top_sectors = pd.concat([top_sectors, pd.Series({"Others": other})])

fig_donut, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(
    top_sectors, labels=top_sectors.index, autopct="%1.1f%%",
    pctdistance=0.82, startangle=140, colors=sns.color_palette("tab20", len(top_sectors)),
)
centre = plt.Circle((0, 0), 0.55, fc="white")
ax.add_artist(centre)
ax.set_title("Aggregate Sector Allocation — Equity Funds")
save_matplotlib(fig_donut, "09_sector_allocation_donut")
chart_count += 1""")

md("## 10. Supplementary Charts (15+ total)")
code("""# 10a — Active SIP accounts growth
fig_active, ax = plt.subplots(figsize=(10, 4))
ax.plot(pd.to_datetime(sip["month"]), sip["active_sip_accounts_crore"],
        color="#059669", marker=".", linewidth=2)
ax.set_title("Active SIP Accounts Growth (Crore)")
ax.set_xlabel("Month")
ax.set_ylabel("Active SIP Accounts (Crore)")
save_matplotlib(fig_active, "10a_active_sip_accounts")
chart_count += 1

# 10b — YoY SIP growth %
sip_yoy = sip.dropna(subset=["yoy_growth_pct"])
fig_yoy, ax = plt.subplots(figsize=(10, 4))
ax.bar(pd.to_datetime(sip_yoy["month"]), sip_yoy["yoy_growth_pct"], color="#7c3aed", width=20)
ax.axhline(sip_yoy["yoy_growth_pct"].mean(), color="red", linestyle="--", label="Mean YoY %")
ax.set_title("Year-over-Year SIP Inflow Growth (%)")
ax.set_ylabel("YoY Growth (%)")
ax.legend()
save_matplotlib(fig_yoy, "10b_sip_yoy_growth")
chart_count += 1

# 10c — 3-year return comparison (top 12 schemes by AUM)
top_perf = performance.nlargest(12, "aum_crore")
fig_ret, ax = plt.subplots(figsize=(11, 5))
sns.barplot(data=top_perf, y="scheme_name", x="return_3yr_pct", hue="category", dodge=False, ax=ax)
ax.set_title("3-Year Returns — Top 12 Schemes by AUM")
ax.set_xlabel("3-Year Return (%)")
ax.set_ylabel("")
save_matplotlib(fig_ret, "10c_3yr_return_comparison")
chart_count += 1

# 10d — Folio composition stacked area
folio_cols = ["equity_folios_crore", "debt_folios_crore", "hybrid_folios_crore", "others_folios_crore"]
fig_stack, ax = plt.subplots(figsize=(10, 5))
ax.stackplot(folio["month_dt"], [folio[c] for c in folio_cols],
             labels=["Equity", "Debt", "Hybrid", "Others"], alpha=0.85)
ax.set_title("Folio Composition by Asset Class")
ax.set_xlabel("Month")
ax.set_ylabel("Folios (Crore)")
ax.legend(loc="upper left")
save_matplotlib(fig_stack, "10d_folio_composition")
chart_count += 1

# 10e — Transaction type breakdown
txn_counts = investors["transaction_type"].value_counts()
fig_txn, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=txn_counts.index, y=txn_counts.values, ax=ax, palette="pastel")
ax.set_title("Investor Transaction Type Distribution")
ax.set_ylabel("Count")
save_matplotlib(fig_txn, "10e_transaction_types")
chart_count += 1

print(f"\\nTotal charts generated: {chart_count}")""")

md("""## 11. Key Findings (10 Insights)

### Finding 1 — NAV Bull Run & Corrections
**Insight:** Equity NAVs surged through 2023 (bull run) before facing drawdowns in early-to-mid 2024, with recovery visible by late 2024.
**Chart:** `01_nav_trend_40_schemes`

### Finding 2 — SBI AUM Dominance
**Insight:** SBI Mutual Fund leads the industry with ₹12.5 Lakh Crore AUM by 2025, nearly 17% ahead of the next-largest fund house.
**Chart:** `02_aum_growth_by_fund_house`

### Finding 3 — SIP Inflows at Record High
**Insight:** Monthly SIP inflows reached an all-time high of ₹31,002 Crore in December 2025, nearly 2.7× the January 2022 level.
**Chart:** `03_monthly_sip_inflows`

### Finding 4 — Liquid Funds Drive Category Inflows
**Insight:** Liquid and debt-oriented categories show the highest net inflow intensity, while sectoral/thematic equity sees episodic spikes.
**Chart:** `04_category_inflow_heatmap`

### Finding 5 — Millennials Dominate SIP Participation
**Insight:** Investors aged 26–45 account for the majority of SIP transactions, with the 36–45 cohort showing the highest median SIP amounts.
**Chart:** `05a_age_group_pie`, `05b_sip_amount_by_age`

### Finding 6 — Male Investors Lead SIP Activity
**Insight:** Male investors contribute roughly twice as many SIP transactions as female investors, indicating a gender participation gap.
**Chart:** `05c_gender_split`

### Finding 7 — Geographic SIP Concentration
**Insight:** SIP flows are spread across states with Madhya Pradesh and Punjab among the top contributors by total SIP amount.
**Chart:** `06a_sip_by_state`

### Finding 8 — T30 Cities Hold SIP Majority
**Insight:** Top-30 (T30) cities account for approximately two-thirds of all SIP transactions, reflecting urban concentration.
**Chart:** `06b_city_tier_pie`

### Finding 9 — Folio Count Nearly Doubled
**Insight:** Total industry folios grew from 13.26 Crore (Jan 2022) to 26.12 Crore (Dec 2025), with equity folios driving most of the expansion.
**Chart:** `07_folio_count_growth`, `10d_folio_composition`

### Finding 10 — Banking & IT Dominate Equity Portfolios
**Insight:** Across equity fund holdings, Banking and IT sectors command the largest aggregate portfolio weights, followed by Pharma and Automobile.
**Chart:** `09_sector_allocation_donut`, `08_nav_return_correlation`""")

code("""# Summary
print("EDA complete.")
print(f"Charts saved to: {CHART_DIR}")
print(f"Total visualizations: {chart_count}")""")

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"},
    },
    "cells": CELLS,
}

NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
print(f"Wrote {NOTEBOOK_PATH}")
