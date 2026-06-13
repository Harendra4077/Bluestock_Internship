import requests
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

scheme_codes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in scheme_codes.items():
    print(f"Fetching NAV for {name} (scheme code: {code})")
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()
    
    if "data" in data:
        nav_history = data["data"]
        df = pd.DataFrame(nav_history)
        output_path = f"data/raw/{name}.csv"
        df.to_csv(output_path, index=False)
        print(f"Successfully saved to {output_path}")
    else:
        print(f"Error fetching data for {name}")
