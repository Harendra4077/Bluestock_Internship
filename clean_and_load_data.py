import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os

os.makedirs("data/processed", exist_ok=True)


def clean_nav_history():
    df = pd.read_csv("data/raw/02_nav_history.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["amfi_code", "date"])
    df = df.drop_duplicates()
    df = df[df["nav"] > 0]
    df = df.reset_index(drop=True)
    df.to_csv("data/processed/nav_history.csv", index=False)
    print("Cleaned nav_history.csv")
    return df


def clean_investor_transactions():
    df = pd.read_csv("data/raw/08_investor_transactions.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_type"] = df["transaction_type"].replace({
        "sip": "SIP",
        "lumpsum": "Lumpsum",
        "redemption": "Redemption"
    })
    df = df[df["amount_inr"] > 0]
    df = df.reset_index(drop=True)
    df.to_csv("data/processed/investor_transactions.csv", index=False)
    print("Cleaned investor_transactions.csv")
    return df


def clean_scheme_performance():
    df = pd.read_csv("data/raw/07_scheme_performance.csv")
    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[(df["expense_ratio_pct"] >= 0.1) & (df["expense_ratio_pct"] <= 2.5)]
    df = df.reset_index(drop=True)
    df.to_csv("data/processed/scheme_performance.csv", index=False)
    print("Cleaned scheme_performance.csv")
    return df


def clean_other_files():
    file_mapping = {
        "01_fund_master.csv": "fund_master.csv",
        "03_aum_by_fund_house.csv": "aum_by_fund_house.csv",
        "04_monthly_sip_inflows.csv": "monthly_sip_inflows.csv",
        "05_category_inflows.csv": "category_inflows.csv",
        "06_industry_folio_count.csv": "industry_folio_count.csv",
        "09_portfolio_holdings.csv": "portfolio_holdings.csv",
        "10_benchmark_indices.csv": "benchmark_indices.csv"
    }
    for src, dest in file_mapping.items():
        df = pd.read_csv(f"data/raw/{src}")
        df.to_csv(f"data/processed/{dest}", index=False)
        print(f"Copied {src} to {dest}")
    return file_mapping


def create_database_schema(engine):
    schema_sql = """
    CREATE TABLE IF NOT EXISTS dim_fund (
        amfi_code INTEGER PRIMARY KEY,
        fund_house TEXT,
        scheme_name TEXT,
        category TEXT,
        sub_category TEXT,
        plan TEXT,
        launch_date TEXT,
        benchmark TEXT,
        expense_ratio_pct REAL,
        exit_load_pct REAL,
        min_sip_amount INTEGER,
        min_lumpsum_amount INTEGER,
        fund_manager TEXT,
        risk_category TEXT,
        sebi_category_code TEXT
    );

    CREATE TABLE IF NOT EXISTS dim_date (
        date TEXT PRIMARY KEY,
        year INTEGER,
        quarter INTEGER,
        month INTEGER,
        day INTEGER,
        day_of_week INTEGER,
        is_weekend BOOLEAN
    );

    CREATE TABLE IF NOT EXISTS fact_nav (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        date TEXT,
        nav REAL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (date) REFERENCES dim_date(date)
    );

    CREATE TABLE IF NOT EXISTS fact_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        investor_id TEXT,
        transaction_date TEXT,
        amfi_code INTEGER,
        transaction_type TEXT,
        amount_inr REAL,
        state TEXT,
        city TEXT,
        city_tier TEXT,
        age_group TEXT,
        gender TEXT,
        annual_income_lakh REAL,
        payment_mode TEXT,
        kyc_status TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
        FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
    );

    CREATE TABLE IF NOT EXISTS fact_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        return_1yr_pct REAL,
        return_3yr_pct REAL,
        return_5yr_pct REAL,
        benchmark_3yr_pct REAL,
        alpha REAL,
        beta REAL,
        sharpe_ratio REAL,
        sortino_ratio REAL,
        std_dev_ann_pct REAL,
        max_drawdown_pct REAL,
        aum_crore REAL,
        expense_ratio_pct REAL,
        morningstar_rating INTEGER,
        risk_grade TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );

    CREATE TABLE IF NOT EXISTS fact_aum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fund_house TEXT,
        aum_crore REAL
    );
    """
    with engine.connect() as conn:
        for statement in schema_sql.split(";"):
            if statement.strip():
                conn.execute(text(statement.strip()))
        conn.commit()
    print("Created database schema")


def load_data_to_sqlite(engine):
    fund_master = pd.read_csv("data/processed/fund_master.csv")
    fund_master.to_sql("dim_fund", engine, if_exists="replace", index=False)

    nav_history = pd.read_csv("data/processed/nav_history.csv", parse_dates=["date"])
    nav_history["date_str"] = nav_history["date"].dt.strftime("%Y-%m-%d")

    dates = pd.DataFrame({"date": nav_history["date_str"].unique()})
    dates_dt = pd.to_datetime(dates["date"])
    dates["year"] = dates_dt.dt.year
    dates["quarter"] = dates_dt.dt.quarter
    dates["month"] = dates_dt.dt.month
    dates["day"] = dates_dt.dt.day
    dates["day_of_week"] = dates_dt.dt.dayofweek
    dates["is_weekend"] = dates_dt.dt.dayofweek >= 5
    dates.to_sql("dim_date", engine, if_exists="replace", index=False)

    fact_nav = nav_history[["amfi_code", "date_str", "nav"]].rename(columns={"date_str": "date"})
    fact_nav.to_sql("fact_nav", engine, if_exists="replace", index=False)

    investor_trans = pd.read_csv("data/processed/investor_transactions.csv", parse_dates=["transaction_date"])
    investor_trans["transaction_date_str"] = investor_trans["transaction_date"].dt.strftime("%Y-%m-%d")
    fact_trans = investor_trans.drop(columns=["transaction_date"]).rename(columns={"transaction_date_str": "transaction_date"})
    fact_trans.to_sql("fact_transactions", engine, if_exists="replace", index=False)

    scheme_perf = pd.read_csv("data/processed/scheme_performance.csv")
    fact_perf_cols = [
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio", "sortino_ratio",
        "std_dev_ann_pct", "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
        "morningstar_rating", "risk_grade"
    ]
    scheme_perf[fact_perf_cols].to_sql("fact_performance", engine, if_exists="replace", index=False)

    aum_df = pd.read_csv("data/processed/aum_by_fund_house.csv")
    aum_df.to_sql("fact_aum", engine, if_exists="replace", index=False)

    print("All data loaded into SQLite database")


def main():
    print("Starting data cleaning process...")
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    clean_other_files()

    print("\nCreating SQLite database...")
    engine = create_engine("sqlite:///bluestock_mf.db")

    create_database_schema(engine)
    load_data_to_sqlite(engine)

    print("\n✅ Data cleaning and database loading complete!")


if __name__ == "__main__":
    main()
