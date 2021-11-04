import pandas as pd

def load_data(path="../csv_combined.csv"):
    return pd.read_csv(path);