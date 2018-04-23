#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Will need to retrieve universe of available currencies from bittrex and place into a pd df
"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import pandas as pd
import requests
import datetime
import io
import numpy as np

class RetrieveMarkets():
    #some global variables for Bittrex
    
    def __init__(self):
        self.api_key='c8f16ead26d4438e991c318c8fd76629'
        self.api_secret='bb885473805547f1834cfc5057a78901'
        self.base_currency='BTC'        

    def getCurrencies(self):
        
        url='https://bittrex.com/api/v1.1/public/getcurrencies'
        #all arguments must be converted to string
        payload={'apikey':self.api_key,
'apisecret':self.api_secret,'nonce':datetime.datetime.now()}

        r=requests.get(url,params=payload)
        df=pd.DataFrame(r.json()['result'])
        self.df_active=df[df.IsActive == True]
    #display this dataframe to the user
        return(self.df_active.loc[:,['Currency','CurrencyLong']])


    def getCurrentPrice(self,ticker_list):
        #consumed by engageUser in the selectExecPrice() which itself is called by eu.prepareTrade()
        url_current='https://bittrex.com/api/v1.1/public/getticker'
#must be a BTC based cross market
        #a list of nested dictionaries
        all_prices_dict={}
        for single_tick in ticker_list:
            self.market=self.base_currency+'-'+single_tick
            #print('sending the trading pair {} to bittrex'.format(self.market))
            payload2={'apikey':self.api_key,
'apisecret':self.api_secret,'nonce':datetime.datetime.now(),'market':self.market}
            r=requests.get(url_current,params=payload2) 
            price_dict=r.json()['result']
            #add the ticker associated w/prices to dict... AS ITS KEY... dict_list will be a list of nested dictionaries
            #TODO have the option of making this a dictionary of dictionaries instead of a list of dictionaries, which is more difficult to index
            #print('response from bittrex {}'.format(price_dict))
            all_prices_dict[single_tick]=price_dict
            
            
        #returns the ask, bid, last trades in a dict/json document... this will be refactored to return a list of dictionaries
        
            
        return(all_prices_dict)
        
    def get24Hr(self, ticker_list):
        url_24_hr='https://min-api.cryptocompare.com/data/histohour?'
        self.stats_dic={}
    
        for single_tick in ticker_list:
            #look up the ticker from the index number
            #instantiate the dicitonary
            self.stats_dic[single_tick]={}
            payload2={'apikey':self.api_key,
'apisecret':self.api_secret,'nonce':datetime.datetime.now(),'fsym':single_tick,'tsym':'BTC','limit':24}
            r=requests.get(url_24_hr,params=payload2) 
            df=pd.DataFrame.from_dict(r.json()['Data'])
            df_mat=df.as_matrix()
            self.stats_dic[single_tick]['max']=np.amax(df_mat[:,1])
            self.stats_dic[single_tick]['min']=np.amin(df_mat[:,1])
            self.stats_dic[single_tick]['avg']=np.average(df_mat[:,1])
        return(self.stats_dic)
    
    def get100Day(self,ticker_index):
        ''' Acquire historical prices from CRYPTOCOMPARE '''
        url='https://min-api.cryptocompare.com/data/histoday'
        #will return a str
        ticker=self.df_active.loc[ticker_index,'Currency']
#prices from last 120 days
        parameters= {'fsym':ticker, 'tsym': self.base_currency, 'e': 'Bittrex', 'aggregate':1,'limit':120}
        
        r=requests.get(url,parameters)
        #handle this error in the calling class
        j_obj=r.json()
        if j_obj['Response']=='Error':
            print("fetch didn't work")
            raise RuntimeError
        raw_time=j_obj['Data']
        df=pd.DataFrame.from_dict(raw_time)
        df['time']=df['time'].apply(lambda x: datetime.datetime.fromtimestamp(x))
        #print the price chart
        self.draw100day(df,ticker)
        #log the ticker elsewhere
        print('get100Day from retrieveMarkets is sending ticker: '+ticker)
        return(ticker)
    
    
    def draw100day(self,df,ticker):
        #calculate the date 100 days ago
        day_100=datetime.datetime.now() - datetime.timedelta(days=100)
        df['ma_20']=df['close'].rolling(20).mean()
        
        plt.subplot(1,1,1)
        plt.xticks(rotation=45)
        plt.xlim(day_100,datetime.datetime.now())
        #plt.plot(df['time'],df['close'],color='red',marker='o')
        plt.plot(df['time'],df['close'],color='green',linestyle='-')
        plt.plot(df['time'],df['ma_20'],color='cyan',linestyle='-')
#plt.title(str(self.market)+' pair') 
        plt.title('100 day and 20 day MA: '+str(self.base_currency)+'-'+ticker+' pair')
        plt.switch_backend('agg')
        plt.show(block=True)
        img=io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plt.close()
        return()
