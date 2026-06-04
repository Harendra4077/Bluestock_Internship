import requests
import pandas as pd
import os

# Create raw folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

scheme_codes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in scheme_codes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    data = response.json()

    df = pd.read_csv("data/raw/fund_master.csv")

    df.to_csv(
        f"data/raw/{name}.csv",
        index=False
    )

    
    print(df["fund_house"].unique())
    print(df["category"].unique())
    print(df["subcategory"].unique())
    print(df["risk_grade"].unique())
    print(df["fund_house"].value_counts())