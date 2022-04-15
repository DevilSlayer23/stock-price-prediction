import requests
import tensorflow as tf
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from keras.layers import Dense,Dropout,LSTM
from sklearn.preprocessing import MinMaxScaler
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from datetime import datetime

def predict():

    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth=True
    sess = tf.compat.v1.Session(config=config)
    path = os.path.join(BASE_DIR, 'nepse1.csv')
    ds=pd.read_csv(path)
    
    df=pd.DataFrame(ds)
    df1=df.reset_index()[['Close']]

    date = df.reset_index()["Date"]
    dates = []
    for a in date:
        dates.append(pd.to_datetime(a).strftime("%Y-%m-%d"))
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format = True)

    #Using MinMaxScaler for normalizing data between 0 & 1
    normalizer = MinMaxScaler(feature_range=(0,1))
    ds_scaled = normalizer.fit_transform(np.array(df1.values).reshape(-1,1))

    #Defining test and train data sizes
    train_size = int(len(ds_scaled)*0.70)
    test_size = len(ds_scaled) - train_size

    #Splitting data between train and test
    ds_train, ds_test = ds_scaled[0:train_size,:], ds_scaled[train_size:len(ds_scaled),:1]


    #creating dataset in time series for LSTM model 
    #X[100,120,140,160,180] : Y[200]
    def create_ds(dataset,step):
        Xtrain, Ytrain = [], []
        for i in range(len(dataset)-step-1):
            a = dataset[i:(i+step), 0]
            Xtrain.append(a)
            Ytrain.append(dataset[i + step, 0])
        return np.array(Xtrain), np.array(Ytrain)

    #Taking 100 days price as one record for training
    time_stamp = 100
    X_train, y_train = create_ds(ds_train,time_stamp)
    X_test, y_test = create_ds(ds_test,time_stamp)


    #Reshaping data to fit into LSTM model
    X_train = X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

    model_path = os.path.join(BASE_DIR, 'model.h5')
    model = load_model(model_path)

    #Predicitng on train and test data
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    #Inverse transform to get actual value
    train_predict = normalizer.inverse_transform(train_predict)
    test_predict = normalizer.inverse_transform(test_predict)
    train_predict
    train_predict_list = train_predict.tolist()
    test_predict_list = test_predict.tolist()
    # original = df1.values.tolist()
    flat_list_train = [item for sublist in train_predict_list for item in sublist]
    flat_list_test = [item for sublist in test_predict_list for item in sublist]
    predicted = flat_list_train + flat_list_test
    original_df = df1.values.tolist()
    original = [item for sublist in original_df for item in sublist]
    # 'original': list(reversed(original)),

    data = {
        'original': list(original), 
        'predicted' : list(predicted),
        'date' : dates,
    }
    return data