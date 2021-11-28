import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data(path="../csv_combined.csv"):
    return pd.read_csv(path);

def preprocess_df(df, name, scale = True, epochs = True):
    """
    Preprocessing logic goes here

    df: input data
    start_halving: where to start off time series data according to bitcoin halving dates (0-4)
    """
    if(df.isnull().sum().count() > 0):
        total_null = df.isnull().sum().count()
        df.dropna(inplace = True)
        print(total_null , ' values have been droped.')
    df.reset_index(inplace=True)    
    df[name] = df[name].astype("datetime64")
    
    if(add_epochs):
        df = add_epochs(df, name)
        
    if(scale):        
        df = scale_df(df, name)
        
#     epoch_to_date = {
#         1: "2012-11-29",
#         2: "2016-07-10",
#         3: "2020-05-12",
#     }

#     if start_halving:
#         df = df[df["Time"] > epoch_to_date[start_halving]]

    return df

def add_epochs(df, name):
    filt = (df[name] >= '2010-08-17') & (df[name] <= '2012-11-28') # start & end
    df1 = df.loc[filt].assign(epoch = float(1))
    filt = (df[name] >= '2012-11-28') & (df[name] <= '2016-07-9') # start & end
    df2 = df.loc[filt].assign(epoch = float(2))
    filt = (df[name] >= '2016-07-9')
    df3 = df.loc[filt].assign(epoch = float(3))
    frames = [df1, df2, df3]
    result = pd.concat(frames)
    return result

def scale_df(df, name, scaler ='MinMax'):
    if(scaler == 'MinMax'):
        columns = df.columns
        scaler = MinMaxScaler()
        scaled_df = scaler.fit_transform(df.drop(['epoch', name], axis =1))
        scaled_df= pd.DataFrame(scaled_df)
        result = pd.concat([ df[name], scaled_df, df['epoch'] ], axis = 1, ignore_index= True)
        result.set_axis(columns, axis = 1, inplace = True)
        return result
    else:
        print('Scaler doesn\'t exist')
        return
        
    
def preprocess_for_prophet(df, predicted_col="close", extra_columns=[]):
    temp_df = df.copy()
    temp_df[["ds", "y"] + extra_columns] = temp_df[["date", predicted_col] + extra_columns]
    return temp_df[["ds", "y"] + extra_columns]