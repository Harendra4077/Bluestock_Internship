
# Bluestock Mutual Fund Analytics Capstone Project

## Project Overview
This project provides a comprehensive analytics platform for mutual fund data, including ETL, exploratory data analysis, performance analytics, advanced risk metrics, and a simple fund recommender system.

## Project Structure
```
Bluestock_Internship/MutualFundProject/
├── clean_and_load_data.py    # Data cleaning and SQLite DB creation
├── data/
│   ├── processed/            # Cleaned data files
│   └── raw/                  # Original raw data files
├── notebooks/
│   ├── EDA_Analytics.ipynb
│   ├── Performance_Analytics.ipynb
│   ├── Advanced_Analytics.ipynb
│   ├── build_eda_notebook.py
│   ├── build_performance_notebook.py
│   ├── build_advanced_notebook.py
│   ├── run_eda.py
│   ├── run_performance.py
│   └── run_advanced.py
├── reports/
│   └── eda_charts/           # Generated charts and visualizations
├── recommender.py            # Simple fund recommendation script
├── run_pipeline.py           # Master execution pipeline
├── bluestock_mf.db           # SQLite database
├── fund_scorecard.csv        # Fund performance scorecard
├── alpha_beta.csv            # Alpha & beta values
└── var_cvar_report.csv       # VaR & CVaR report
```

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the full pipeline:
   ```bash
   python run_pipeline.py
   ```

## Data Sources
The project uses 10 datasets for mutual fund analytics:
1. fund_master.csv - Master fund details (AMFI code, scheme name, category, etc.)
2. nav_history.csv - Daily NAV data for all funds
3. aum_by_fund_house.csv - Assets Under Management by fund house
4. monthly_sip_inflows.csv - Monthly SIP inflow data
5. category_inflows.csv - Net inflows by fund category
6. industry_folio_count.csv - Industry folio count trends
7. investor_transactions.csv - Investor transaction details
8. portfolio_holdings.csv - Fund portfolio holdings
9. benchmark_indices.csv - Benchmark index data (NIFTY50, NIFTY100, etc.)
10. scheme_performance.csv - Scheme performance metrics

## Notebooks
1. **EDA_Analytics.ipynb** - Exploratory Data Analysis with 18+ charts
2. **Performance_Analytics.ipynb** - Performance metrics: CAGR, Sharpe, Sortino, Alpha/Beta, Max Drawdown, Scorecard
3. **Advanced_Analytics.ipynb** - Advanced analytics: VaR/CVaR, Rolling Sharpe, Cohort Analysis, SIP Continuity, HHI Concentration

## Fund Recommender
Run the fund recommender script to get top 3 funds based on your risk appetite:
```bash
python recommender.py
```
Options: "Low", "Moderate", "High" risk appetite

## Dashboard (Day 5)
To create the Power BI/Tableau dashboard:
1. Connect to cleaned data files in `data/processed/` or to `bluestock_mf.db` via SQLite ODBC
2. Create 4 pages as described in Day5_Dashboard_Guide.md
3. Export as .pbix/.twbx, PDF, and page screenshots

## Key Deliverables
- ✅ Day 1-2: Data Ingestion & Cleaning
- ✅ Day 3: EDA Analysis & 18+ charts
- ✅ Day 4: Performance Analytics, scorecard, benchmark chart
- ✅ Day 5: Dashboard Guide
- ✅ Day 6: Advanced Analytics & Recommender
- ✅ Day 7: Final Report, Pipeline, README

## Technologies Used
- Python (pandas, numpy, matplotlib, seaborn, scipy)
- SQLite (database)
- Jupyter Notebooks
- (Optional) Power BI / Tableau for dashboard
