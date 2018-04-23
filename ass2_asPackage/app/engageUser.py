#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Client dialogue
"""
import sys
sys.path.append('/usr/src/app/PROJECT_FOLDER')
import tradeClass as trade
import ass1_acountsClass as accts
import datetime as datetime
import tradeManager as tm
from retrieveMarkets import RetrieveMarkets

class Dialogue(object):
    def __init__(self):
        self.todayTrading=tm.TradingDay()
        #create a new account/portfolio
        self.act=accts.Account()
    
    def engageUser(self):
        menuSelection=input('Please select from the list of options below.\n a -Trade\n b - Show Blotter\n c- Show P/L\n d - Quit\n > ')
        if menuSelection=='a':
            self.prepareTrade()
        elif menuSelection=='b':
            #call the blotter from the tradeManager class - may need rendering in this class, and the return value from either this function or another in this class can be handled at the controller level
            # TODO print('call blotter function')
            #the blotter function will return a list of dictionaries, or perhaps a pandas dataframe, that I'll then print... if extensive formating is required, I'll do it in this class
            print(self.todayTrading.prettyPrintTradeLog())
            return(self.engageUser())
        elif menuSelection=='c':
            
            print('your current portfolio is below... p&l calc is pending')
            self.calcPL()
            
            return self.engageUser()
        elif menuSelection=='d':
            return
        else:
            print('please select an option')
            self.engageUser()
    
    def iterateDF(self,df,index_start):
        #begin iteration from the index passed in the argument call
        g=index_start
        increment=35
        print(df.loc[:,['Currency','CurrencyLong']].iloc[g:g+increment])
        g=g+increment
        user_input=input('which coin would you like to trade? Please type the index number corresponding with the coin symbol.\n> ')
        if user_input=='n':
            while user_input=='n' and   g<df.shape[0]+(increment-2):
                print(df.loc[:,['Currency','CurrencyLong']].iloc[g:g+increment])
                g=g+increment
                user_input=input('> ')
            #TODO user_input ne 'n' breaks the loop, must then evaluate the user input
            #TODO do I need to return the series, or ticker, or nothing?
        return(user_input,g)
    
    def qaAndSelect(self,shapes,userInput):
        #evaluate user input
        try:
            lookup_index=int(userInput)
            if (lookup_index < shapes and int(lookup_index)>-1):
                return(True)
            else:
                return(False)
        except ValueError:
            #user did not enter an appropriate value
            print("please type an integer or the letter 'n'")
            return(False)
            
    def prepareTrade(self):
        #aggDic will be the dictionary that stores trade details and later passes to fa
            agg_dic={}            
            #dictionary of trade stats to send over to the tradeClass
            self.rm=RetrieveMarkets()
            df_active=self.rm.getCurrencies()
            g=False
            iterate_index=1
            while g==False:
                user_input,iterate_index=self.iterateDF(df_active,iterate_index)
                g=self.qaAndSelect(df_active.shape[0],user_input)
                    #TODO ticker now in hand... must handle
            #render 100-day chart and return the ticker
            ticker=self.rm.get100Day(int(user_input))
            #assume that user_input is a string
            result_dic=self.rm.get24Hr([ticker])
            print(result_dic[ticker])
                    
                    #AFTER TICKER IS SELECTED
            try:
                #TODO need to update this process, as the explicit ticker is not stored in the engageUser object
                #begin forming the trade dictionary
                agg_dic['ticker']=ticker
            except KeyError:
                print('incorrect selection')
                #start over
                self.engageUser()
     
            tradeDirection=input('Would you like to\n a- buy\n b- sell to close\n > ') #drives whether we calculate using bid or ask
            #trade direction is a string: theoretically either a or b
            try:
                print(ticker)
                agg_dic['tradetype'],agg_dic['price']=self.selectExecPrice(tradeDirection,ticker)
            except ValueError:
                self.engageUser()
            
            #The user is then asked to confirm the trade at the market ask price scraped from Yahoo.
            cont=input('You can transact at {} {}. Would you like to continue y/n?\n > '.format(agg_dic['price'],self.rm.base_currency))
            
            if cont=='y':
                #send over this data to the tradeClass or can return a dictionary
                qty=float(input('How many target coins would you like to trade into?\n > '))
                agg_dic['coins']=qty    
                agg_dic['timestamp']=datetime.datetime.now()
                print('Your trade is being processed')
                #TODO record trade details and verify validity (by interacting with the account class)... recall that it's the tradeManager that will store/send the trades to the mongoDB
                try:
                    #makeTrade now also posts the trade to the accounts object
                    single_trade_dic=self.todayTrading.makeTrade(agg_dic,self.act)
                    #print(single_trade_dic)
                    #direct interface with accounts class
                    #self.act.postEquityTrade(single_trade_dic)
                    print('post trade positions:')
                    print(self.act.positions)
                    self.engageUser() 
            #engage user again                    
            #TODO replace KeyError with ValueError
                except KeyError:
                    print('try a valid trade')
                    self.engageUser()
            else: #if user selects anything other than 'yes'
                self.engageUser()
            
        
            
                #acount object has now been updated at the highest scope
                #trade.EquityTrade(agg_dic,self.act)
                
                
                #TODO discover the error below, an invalid trade is being sent to act.CheckIfNew, but should die at the tradeClass... ensure that the call to makeTrade() encounters the invalid trade error... enforce that the thrown error reaches this object
                
                
                    #makeTrade() calls tradeClass.tradeType() which QAs the trade, determines the original tradetype (long/short) and calculates the delta on position size and imapct to cash
                     #TODO printing None
                
                #TODO this is the portion that is explicitly throwing the error... error states that single_trade_dic is empty
                    
                #keep the session going until the user quits
                
                
                
    def selectExecPrice(self,letter,ticker):
        #handle the user trade request and lookup the proper price
        #print('ticker as recognized by selectExecPrice in eu: '+ticker)
        #a lookup dictionary
        options={'a':'buy','b':'sell to close'}
            
        try:
                #TODO call the retrieveMarkets class... then call TradeManager which calls TradeClass... getCurrentPrice() now requires a list of tickers - one is fine
            current_price_dict=self.rm.getCurrentPrice([ticker])[ticker]
            
            #select the appropriate price according to the trade type: buy on ask and sell on the bid
            map_bid_ask={'a':'Ask','b':'Bid'}
            appPrice=current_price_dict[map_bid_ask[letter]]
            #return a tuple of the transaction type and the applicable market price
            return(options[letter],appPrice)
        except ValueError:
            print('type either a or b')
            raise ValueError
            
            
    def calcPL(self):
        #call scraper, pass dictionary of current prices to the account object and print the current status of the portfolio dictionary, equipped with both realized and unrealized p+l
        #ideally, get all the tickers from the accounts class, then pass an array to retrieveMarkets class
        #this should be coin tickers
        #print('acquiring keys from the accounts portfolio df')
        #print(self.act.positions.keys())
        #keys function returns a list
        ticker_array=self.act.positions.keys()
        if len(ticker_array)>0:
            
        #verified this works independent of the program
            prices_dict=self.rm.getCurrentPrice(ticker_array)
        
        
        #TODO sortedTrades relies on the old tuple format and not the new mongoDB... sortTrades() returns a 
        #TODO call the tradeManager class to retrieve the trade blotter and return a unique list of tickers in order of trade activity
        #TODO ensure that set() accepts a pd.Series... has the benefit of storing only unique values... even then, need to ensure that the latest entry of a given ticker is preserved.
            #print('acquiring ordered portfolio')
            sorted_list=self.todayTrading.prettyPrintTradeLog().sort_values(['ticker'])['ticker'].unique()
            #print('sorted potfolio is {}'.format(sorted_list))
            #print('moving on the last step: act.calcUPL - called from eu.calcPL')
        
        #TODO undo print(self.act.calcUPL(prices_dict,sorted_list))
            print(self.act.calcUPL(prices_dict,sorted_list))
        else:
            print('Your cash balance is {}'.format(self.act.coin_bal))
        return
