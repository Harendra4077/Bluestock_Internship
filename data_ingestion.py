import pandas as pd
import os

data_folder = "data/raw"


print("Current Working Directory:", os.getcwd())
print("Data Folder Exists:", os.path.exists(data_folder))

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        path = os.path.join(data_folder, file)

        df = pd.read_csv(path)

        print("\n" + "="*50)
        print(f"FILE: {file}")

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())