
"""Generate Performance_Analytics.ipynb for Day 4 capstone deliverable."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = Path(__file__).resolve().parent / "Performance_Analytics.ipynb"

CELLS = []


def md(source: str):
    CELLS.append({"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)})


def code(source: str):
    CELLS.append({"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
                  "source": source.splitlines(keepends=True)})


md("""# DAY 4 - Fund Performance Analytics
## Capstone Project I - Mutual Fund Analytics

This notebook calculates key performance metrics for mutual funds, including daily returns, CAGR, Sharpe Ratio, Sortino Ratio, Alpha, Beta, Maximum Drawdown, and a composite Fund Scorecard.

**Deliverables**: Performance_Analytics.ipynb, fund_scorecard.csv, alpha_beta.csv, benchmark comparison chart PNG""")

code("""import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.optimize import minimize

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight", "font.size": 10})

ROOT = next(
    (p for p in [Path.cwd(), *Path.cwd().parents] if (p / "data" / "processed" / "fund_master.csv").exists()),
    Path.cwd(),
)
DATA = ROOT / "data" / "processed"
OUTPUT = ROOT / "reports" / "eda_charts"
OUTPUT.mkdir(parents=True, exist_ok=True)

def save_matplotlib(fig, name):
    path = OUTPUT / f"{name}.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved {path.name}")

print("Setup complete")
""")

code("""# Load datasets
fund_master = pd.read_csv(DATA / "fund_master.csv")
nav_history = pd.read_csv(DATA / "nav_history.csv", parse_dates=["date"])
benchmark_indices = pd.read_csv(DATA / "benchmark_indices.csv", parse_dates=["date"])
scheme_performance = pd.read_csv(DATA / "scheme_performance.csv")

print(f"Loaded {fund_master['amfi_code'].nunique()} funds")
print(f"NAV history: {nav_history.shape}")
print(f"Benchmarks: {benchmark_indices['index_name'].unique()}")
""")

md("""## 1. Compute Daily Returns for All Schemes""")

code("""# Compute daily returns
nav_history = nav_history.sort_values(['amfi_code', 'date']).copy()
nav_history['daily_return'] = nav_history.groupby('amfi_code')['nav'].pct_change()

print("Daily returns computed for all schemes")
print(nav_history[['amfi_code', 'date', 'nav', 'daily_return']].head())
""")

md("""## 2. Compute CAGR for 1yr, 3yr, 5yr for All Funds""")

code("""def calculate_cagr(series, years):
    \"\"\"Calculate Compound Annual Growth Rate\"\"\"
    if len(series) < 2:
        return np.nan
    start_value = series.iloc[0]
    end_value = series.iloc[-1]
    if start_value <= 0 or end_value <= 0:
        return np.nan
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr

# Get date range
start_date = nav_history['date'].min()
end_date = nav_history['date'].max()
total_years = (end_date - start_date).days / 365.25
print(f"Data range: {start_date.date()} to {end_date.date()} ({total_years:.1f} years)")

# Calculate CAGRs
cagr_results = []
for amfi_code in nav_history['amfi_code'].unique():
    fund_nav = nav_history[nav_history['amfi_code'] == amfi_code].set_index('date')['nav']
    cagr_1yr = calculate_cagr(fund_nav, 1) if total_years >= 1 else np.nan
    cagr_3yr = calculate_cagr(fund_nav, 3) if total_years >= 3 else np.nan
    cagr_5yr = calculate_cagr(fund_nav, 5) if total_years >= 5 else np.nan
    
    cagr_results.append({
        'amfi_code': amfi_code,
        'cagr_1yr_pct': cagr_1yr * 100 if not pd.isna(cagr_1yr) else np.nan,
        'cagr_3yr_pct': cagr_3yr * 100 if not pd.isna(cagr_3yr) else np.nan,
        'cagr_5yr_pct': cagr_5yr * 100 if not pd.isna(cagr_5yr) else np.nan,
    })

cagr_df = pd.DataFrame(cagr_results)
cagr_df = cagr_df.merge(fund_master[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
print("CAGR computation complete:")
print(cagr_df.head())
""")

md("""## 3. Compute Sharpe Ratio (Rf = 6.5%)""")

code("""RISK_FREE_RATE = 0.065  # 6.5% annual
TRADING_DAYS = 252

def calculate_sharpe_ratio(returns, risk_free_rate=RISK_FREE_RATE):
    \"\"\"Calculate Sharpe Ratio using daily returns\"\"\"
    excess_returns = returns - (risk_free_rate / TRADING_DAYS)
    if len(excess_returns) < 2:
        return np.nan
    sharpe = np.sqrt(TRADING_DAYS) * excess_returns.mean() / excess_returns.std()
    return sharpe

sharpe_results = []
for amfi_code in nav_history['amfi_code'].unique():
    fund_returns = nav_history[nav_history['amfi_code'] == amfi_code]['daily_return'].dropna()
    sharpe = calculate_sharpe_ratio(fund_returns)
    sharpe_results.append({
        'amfi_code': amfi_code,
        'sharpe_ratio': sharpe
    })

sharpe_df = pd.DataFrame(sharpe_results)
sharpe_df = sharpe_df.merge(fund_master[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
print("Sharpe Ratio computation complete:")
print(sharpe_df.head())
""")

md("""## 4. Compute Sortino Ratio (Downside Deviation)""")

code("""def calculate_sortino_ratio(returns, risk_free_rate=RISK_FREE_RATE):
    \"\"\"Calculate Sortino Ratio using daily returns\"\"\"
    excess_returns = returns - (risk_free_rate / TRADING_DAYS)
    downside_returns = excess_returns[excess_returns < 0]
    if len(downside_returns) < 2:
        return np.nan
    downside_dev = np.sqrt(np.mean(downside_returns**2))
    sortino = np.sqrt(TRADING_DAYS) * excess_returns.mean() / downside_dev
    return sortino

sortino_results = []
for amfi_code in nav_history['amfi_code'].unique():
    fund_returns = nav_history[nav_history['amfi_code'] == amfi_code]['daily_return'].dropna()
    sortino = calculate_sortino_ratio(fund_returns)
    sortino_results.append({
        'amfi_code': amfi_code,
        'sortino_ratio': sortino
    })

sortino_df = pd.DataFrame(sortino_results)
sortino_df = sortino_df.merge(fund_master[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
print("Sortino Ratio computation complete:")
print(sortino_df.head())
""")

md("""## 5. Compute Alpha & Beta vs NIFTY100""")

code("""# Prepare benchmark data
nifty100 = benchmark_indices[benchmark_indices['index_name'] == 'NIFTY100'].copy()
nifty100 = nifty100.sort_values('date').reset_index(drop=True)
nifty100['benchmark_return'] = nifty100['close_value'].pct_change()
nifty100 = nifty100[['date', 'benchmark_return']].dropna()

def calculate_alpha_beta(fund_returns_df, benchmark_df):
    \"\"\"Calculate Alpha & Beta using OLS regression\"\"\"
    # Merge fund returns with benchmark
    merged = fund_returns_df[['date', 'daily_return']].merge(
        benchmark_df, on='date', how='inner'
    ).dropna()
    if len(merged) < 30:
        return np.nan, np.nan
    
    # OLS regression
    x = merged['benchmark_return'].values
    y = merged['daily_return'].values
    beta, alpha, r_value, p_value, std_err = stats.linregress(x, y)
    # Annualize alpha
    alpha_annual = alpha * TRADING_DAYS * 100
    return alpha_annual, beta

alpha_beta_results = []
for amfi_code in nav_history['amfi_code'].unique():
    fund_data = nav_history[nav_history['amfi_code'] == amfi_code].copy()
    alpha, beta = calculate_alpha_beta(fund_data, nifty100)
    alpha_beta_results.append({
        'amfi_code': amfi_code,
        'alpha_pct': alpha,
        'beta': beta
    })

alpha_beta_df = pd.DataFrame(alpha_beta_results)
alpha_beta_df = alpha_beta_df.merge(fund_master[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
print("Alpha & Beta computation complete:")
print(alpha_beta_df.head())
""")

md("""## 6. Compute Maximum Drawdown""")

code("""def calculate_max_drawdown(nav_series):
    \"\"\"Calculate Maximum Drawdown and date range\"\"\"
    nav_series = nav_series.copy()
    # Calculate running maximum
    running_max = nav_series.cummax()
    # Calculate drawdown
    drawdown = (nav_series - running_max) / running_max
    # Find max drawdown
    max_dd = drawdown.min()
    if pd.isna(max_dd):
        return np.nan, np.nan, np.nan
    
    # Find peak and trough dates
    peak_idx = drawdown.idxmin()
    trough_idx = peak_idx
    peak_idx = nav_series.loc[:peak_idx].idxmax()
    
    return max_dd * 100, peak_idx.date(), trough_idx.date()

mdd_results = []
for amfi_code in nav_history['amfi_code'].unique():
    fund_nav = nav_history[nav_history['amfi_code'] == amfi_code].set_index('date')['nav']
    mdd_pct, peak_date, trough_date = calculate_max_drawdown(fund_nav)
    mdd_results.append({
        'amfi_code': amfi_code,
        'max_drawdown_pct': mdd_pct,
        'peak_date': peak_date,
        'trough_date': trough_date
    })

mdd_df = pd.DataFrame(mdd_results)
mdd_df = mdd_df.merge(fund_master[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
print("Maximum Drawdown computation complete:")
print(mdd_df.head())
""")

md("""## 7. Build Fund Scorecard (0-100)""")

code("""# Merge all metrics
scorecard = fund_master[['amfi_code', 'scheme_name', 'fund_house', 'category', 'expense_ratio_pct']].copy()
scorecard = scorecard.merge(cagr_df[['amfi_code', 'cagr_3yr_pct']], on='amfi_code', how='left')
scorecard = scorecard.merge(sharpe_df[['amfi_code', 'sharpe_ratio']], on='amfi_code', how='left')
scorecard = scorecard.merge(alpha_beta_df[['amfi_code', 'alpha_pct']], on='amfi_code', how='left')
scorecard = scorecard.merge(mdd_df[['amfi_code', 'max_drawdown_pct']], on='amfi_code', how='left')

# Calculate ranks for scoring
scorecard['cagr_rank'] = scorecard['cagr_3yr_pct'].rank(pct=True, ascending=True) * 100
scorecard['sharpe_rank'] = scorecard['sharpe_ratio'].rank(pct=True, ascending=True) * 100
scorecard['alpha_rank'] = scorecard['alpha_pct'].rank(pct=True, ascending=True) * 100
scorecard['expense_rank'] = scorecard['expense_ratio_pct'].rank(pct=True, ascending=False) * 100  # Lower expense is better
scorecard['mdd_rank'] = scorecard['max_drawdown_pct'].rank(pct=True, ascending=False) * 100  # Lower drawdown is better

# Calculate composite score (weights as per requirements)
scorecard['fund_score'] = (
    0.30 * scorecard['cagr_rank'] +
    0.25 * scorecard['sharpe_rank'] +
    0.20 * scorecard['alpha_rank'] +
    0.15 * scorecard['expense_rank'] +
    0.10 * scorecard['mdd_rank']
)

# Sort by score descending
scorecard = scorecard.sort_values('fund_score', ascending=False).reset_index(drop=True)
scorecard['rank'] = scorecard.index + 1
print("Fund Scorecard complete:")
print(scorecard.head(10))
""")

md("""## 8. Benchmark Comparison Chart (Top 5 vs NIFTY50/NIFTY100)""")

code("""# Get top 5 funds by score
top5_funds = scorecard.head(5)['amfi_code'].tolist()
top5_names = scorecard.head(5)['scheme_name'].tolist()

# Prepare data for chart
chart_data = []
for amfi_code in top5_funds:
    fund_data = nav_history[nav_history['amfi_code'] == amfi_code][['date', 'nav']].copy()
    fund_data = fund_data.sort_values('date').reset_index(drop=True)
    # Normalize to 100 at start
    fund_data['normalized'] = (fund_data['nav'] / fund_data['nav'].iloc[0]) * 100
    chart_data.append(fund_data[['date', 'normalized']].rename(columns={'normalized': f'fund_{amfi_code}'}))

# Add NIFTY50
nifty50 = benchmark_indices[benchmark_indices['index_name'] == 'NIFTY50'].copy()
nifty50 = nifty50.sort_values('date').reset_index(drop=True)
nifty50['normalized'] = (nifty50['close_value'] / nifty50['close_value'].iloc[0]) * 100
chart_data.append(nifty50[['date', 'normalized']].rename(columns={'normalized': 'NIFTY50'}))

# Add NIFTY100
nifty100_chart = benchmark_indices[benchmark_indices['index_name'] == 'NIFTY100'].copy()
nifty100_chart = nifty100_chart.sort_values('date').reset_index(drop=True)
nifty100_chart['normalized'] = (nifty100_chart['close_value'] / nifty100_chart['close_value'].iloc[0]) * 100
chart_data.append(nifty100_chart[['date', 'normalized']].rename(columns={'normalized': 'NIFTY100'}))

# Merge all data
benchmark_df = chart_data[0]
for df in chart_data[1:]:
    benchmark_df = benchmark_df.merge(df, on='date', how='outer')

# Plot
fig, ax = plt.subplots(figsize=(14, 7))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#7f7f7f', '#bcbd22']
for i, (col, color) in enumerate(zip(benchmark_df.columns[1:], colors)):
    label = top5_names[i] if i < 5 else col
    ax.plot(benchmark_df['date'], benchmark_df[col], label=label, linewidth=2 if col in ['NIFTY50', 'NIFTY100'] else 1.5, color=color)

ax.set_title('Top 5 Funds vs Benchmarks (Normalized to 100)', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Normalized Value', fontsize=12)
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
save_matplotlib(fig, 'top5_vs_benchmark')
plt.show()
""")

md("""## 9. Save Deliverables""")

code("""# Save scorecard
scorecard.to_csv(DATA.parent / 'fund_scorecard.csv', index=False)
print(f"Saved fund_scorecard.csv to {DATA.parent}")

# Save alpha_beta
alpha_beta_df.to_csv(DATA.parent / 'alpha_beta.csv', index=False)
print(f"Saved alpha_beta.csv to {DATA.parent}")

print("All deliverables saved successfully!")
""")

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
