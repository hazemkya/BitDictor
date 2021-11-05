import pandas as pd

def load_data(path="../csv_combined.csv"):
    return pd.read_csv(path);

def preprocess_df(df, start_halving=2):
    """
    Preprocessing logic goes here

    df: input data
    start_halving: where to start off time series data according to bitcoin halving dates (0-4)
    """
    df["Time"] = df["Time"].astype("datetime64")

    epoch_to_date = {
        1: "2012-11-29",
        2: "2016-07-10",
        3: "2020-05-12",
    }

    if start_halving:
        df = df[df["Time"] > epoch_to_date[start_halving]]

    return df

def preprocess_for_prophet(df, predicted_col="day_close", extra_columns=[]):
    temp_df = pd.DataFrame(df)
    temp_df[["ds", "y"] + extra_columns] = temp_df[["Time", predicted_col] + extra_columns]
    return temp_df[["ds", "y"] + extra_columns]