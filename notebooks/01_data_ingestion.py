import pandas as pd
import os

files = [
    "10_benchmark_indices.csv",
    "09_portfolio_holdings.csv",
    "08_investor_transactions.csv",
    "07_scheme_performance.csv",
    "06_industry_folio_count.csv",
    "05_category_inflows.csv",
    "04_monthly_sip_inflows.csv",
    "03_aum_by_fund_house.csv",
    "02_nav_history.csv",
    "01_fund_master.csv"
]

for file in files:
    print(f"\n{'='*50}")
    print(f"Checking {file}")

    df = pd.read_csv(f"data/raw/{file}")

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Records:")
    print(df.duplicated().sum())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)