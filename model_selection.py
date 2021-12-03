import pandas as pd
import numpy as np
import json
from importlib.machinery import SourceFileLoader
from prophet.serialize import model_from_json


def get_prediction(days):
    utilities = SourceFileLoader(
        "utilities", "model/utilities.py").load_module()

    df = utilities.load_data('csv_combined.csv')
    df = utilities.preprocess_df(df, 'Time', scale=False)

    with open(f'saves/model for 100days.json', 'r') as fin:
        pf = model_from_json(json.load(fin))  # Load model

    future = pf.make_future_dataframe(periods=days, freq='1D')
    ndf = df.drop(['Time'], axis=1)
    frames = [future, ndf]
    final = pd.concat(frames, axis=1)
    final.dropna(inplace=True)

    data = pf.predict(final)
    print('done predicting..')
    time_merged, close_merged = merge_data(df, data)
    predicted = to_list(time_merged, close_merged, days)
    close_merged = close_merged.round(0)
    time_merged = time_merged.astype(str)
    close_merged = close_merged.astype(int)
    print('done get prediction..')

    return list(time_merged), np.array(close_merged), predicted


def to_list(time_merged, close_merged, days):
    predicted = pd.concat([time_merged, close_merged],
                          axis=1, ignore_index=True)
    predicted = predicted.set_axis(['date', 'price'], axis='columns')
    predicted['price'] = predicted['price'].round(2)
    predicted.reset_index(drop=True, inplace=True)
    predicted = predicted.loc[len(predicted)-days:]
    predicted = predicted.astype(str)
    predicted.reset_index(drop=True, inplace=True)
    predicted = list(predicted.itertuples(index=False, name=None))

    return predicted


def merge_data(df, data):
    close = df['day_close']
    yhat = data['yhat']
    close_merged = pd.concat([close, yhat.loc[len(yhat)-2:]])

    Time = df['Time']
    ds = data['ds']
    time_merged = pd.concat([Time, ds.loc[len(ds)-2:]])
    return time_merged, close_merged
