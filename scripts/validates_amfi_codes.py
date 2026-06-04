import pandas as pd

fund_master = pd.read_csv("data/raw/01_fund_master.csv")
nav_history = pd.read_csv("data/raw/02_nav_history.csv")

missing_codes = set(
    fund_master["amfi_code"]
) - set(
    nav_history["amfi_code"]
)

print("Missing Codes:")
print(missing_codes)