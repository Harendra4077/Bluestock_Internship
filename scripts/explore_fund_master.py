import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/01_fund_master.csv")

# Basic information
print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

# Unique values
print("\nFund Houses:")
print(df["fund_house"].unique())

print("\nCategories:")
print(df["category"].unique())

print("\nSub categories:")
print(df["sub_category"].unique())

print("\nRisk Categories:")
print(df["risk_category"].unique())

# Counts
print("\nFund House Counts:")
print(df["fund_house"].value_counts())