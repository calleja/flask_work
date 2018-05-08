#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 18:45:29 2018

@author: lechuza
"""
import sys
sys.path.append('/home/lechuza/Documents/CUNY/data_607/ass3_production')
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import pandas as pd
from app.forecasts import Forecast


f=Forecast()
var_df=f.prepareDF('ETH')
var_df.iloc[-1:]
lags=1 #applying three lags
var_df1=var_df.dropna(how='any')[['mid','vol_3day','vol_15day','prop2','prop5','prop15']]
#removing 'mid'

var_df1.dtypes
var_df1['mid'].tail()
#verify this
all_X=var_df1.iloc[:,1:]
all_Y=var_df1.iloc[:,0]
all_Y=all_Y.reshape(all_Y.shape[0],1)
all_Y[-4:]

scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(all_X)
df=pd.DataFrame(scaled,columns=all_X.columns)
values = df.values

scaler1 = preprocessing.MinMaxScaler(feature_range=(0, 1))
scaled1 = scaler1.fit_transform(all_Y)
df1=pd.DataFrame(scaled1,columns=['dependent'])
values1 = df1.values

#we can partition this now... will wait to partition the training set after the performing the lag
idependent_test=values[-1,:]

#run the lag on only the independent values
lista=[]
for i in np.arange(1,lags+1,1):
    temp_df=df.shift(+1,axis=0)
    temp_df.columns=['var'+str(counter+1)+'(t-{})'.format(i) for counter, h in enumerate(temp_df.columns)]
    lista.append(temp_df)

#430 records    
agg_df=pd.concat(lista,axis=1)
agg_df['var(t)']=values1
#for QA, compare with var_df1


agg_df.dropna(how='any',inplace=True)

# split into input and outputs... use all the data available to train
independent_train=agg_df.values.astype('float32')[:,:-1]
dependent_train=agg_df.values.astype('float32')[:,-1]
independent_train.shape

# reshape input to be 3D [samples, timesteps, features]
train_X = independent_train.reshape((independent_train.shape[0], 1, independent_train.shape[1]))
#while I'm at it, I will transform the out-of-sample data
test_X = idependent_test.reshape((1,1,idependent_test.shape[0]))


mdl = Sequential()
mdl.add(Dense(3, input_shape=(train_X.shape[1], train_X.shape[2]), activation='relu'))
mdl.add(LSTM(6, activation='relu'))
mdl.add(Dense(1, activation='relu'))
mdl.compile(loss='mean_squared_error', optimizer='adam')
mdl.fit(train_X, dependent_train, epochs=30, batch_size=1, verbose=0)

#with model in hand, let's fit the prediction
test_predict = mdl.predict(test_X,verbose=0)
#concatenate with the training dependent:
y_reunited=np.concatenate((dependent_train,test_predict[0]),axis=0)
y_reunited=y_reunited.reshape(y_reunited.shape[0],1)

#inverse transform the output and get in same units as the input

inv_agg_data=scaler1.inverse_transform(y_reunited)
inv_agg_data[-1,:][0]

