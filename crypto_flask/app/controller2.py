#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controller class to the equity trading platform
"""
from app import app
from flask import render_template, flash, redirect, request, session
from app.mainForm import  MainMenuForm
from app.cryptoMenu import CryptoMenuForm
from app import engageUser as eu
from app import retrieveMarkets, tradeDeetsForm
import os

eud=eu.Dialogue()

@app.route('/')
def landing(methods=['GET']):
    session['number']=0
    return render_template('landing_page.html')

@app.route('/main_menu',methods=['GET','POST'])
def mainMenu():
#will need to handle the selection of the form
    form=MainMenuForm()
    if request.method == 'POST':
		#TODO don't understand redirect...
        if form.menu_selection.data=='a':
            return(redirect('/crypto_menu'))
        #eud.engageUser(form.menu_selection.data)
        elif form.menu_selection.data=='b':
            #trade blotter
            return(redirect('/trade_blotter'))
        elif form.menu_selection.data=='d':
            return(redirect('/coin_trade_history'))
        return(redirect('/main_menu'))
	#handle the rendering 
    return(render_template('main_menu_crypt.html', title='Main Menu', form=form))
	
index_start=0
    
@app.route('/crypto_menu',methods=['GET','POST'])
def cryptoMenu():
    #engage the user on asset, transaction type, number of shares 
    rm=retrieveMarkets.RetrieveMarkets()
    session['number']==0
    df_active=rm.getCurrencies()
    df_active.reset_index(inplace=True)
    session['cryptos']=df_active.to_dict('records')
    #loop through this list of dictionaries
    if request.method== 'GET':
        session['number']==0
    g=session['number']
    increment=35
    subsection=session['cryptos'][g:g+increment]
    cform=CryptoMenuForm()      
    
    #if the next button was clicked... first iteration will be executed after the first set of currencies have been rendered
    if request.method== 'POST':
        if cform.nexty.data:
        #first create indexing range
            session['number'] +=1
            g=session['number']*increment
            subsection=session['cryptos'][g:g+increment]
            return(render_template('index_crypt.html', title='Main Menu', menu=subsection, form=cform))
        elif cform.submit.data:
            #an asset has been selected... store it in a session variable
            session['trade_dict']={'ticker_index':cform.str_selection.data}
            session['trade_dict']['ticker']=df_active.iloc[int(cform.str_selection.data),1]
            return(redirect('/trade_details'))
    #first rendering with a GET request
    flash('running this {}'.format(request.method))
    return(render_template('index_crypt.html', title='Main Menu', menu=subsection, form=cform))
    
            
@app.route('/trade_details',methods=['GET','POST'])            
def enquireDeets():
    form=tradeDeetsForm.TradeDetailsForm()
    #need to return a chart graphic and the current price of the ticker... the user can control this by selecting one of two buttons: view market stats and submit trade
    #rm=retrieveMarkets.RetrieveMarkets()
    if form.viewstats.data:
        #user elects to view stats, and not yet submit trade; render the prevailing market price and price chart
        #the below has dependencies: a) session['trade_dict']['ticker'] b) form.coinFreqString; c)form.tradeRadio.data
        flash('session ticker: {}'.format(session['trade_dict']['ticker']))
        flash('this is form.tradeRadio.data {}'.format(form.tradeRadio.data))
        try:
            mkt_price,image_url=eud.engageUser('a',ticker=session['trade_dict']['ticker'],tradetype=form.tradeRadio.data)
            flash('market price was retrieved and stored successfully at {}'.format(mkt_price))
            flash('image url was properly generated as {}'.format(image_url))
        except TypeError:
            mkt_price= str(100.00)
            image_url=os.getcwd()+'/image_1.png'
        #flash('market price: {}'.format(mkt_price))
        #flash('image url: {}'.format(image_url))
        #retrieve the graphic
        #image_url=rm.get100Day(session['trade_dict']['ticker'])
        #must pass the returned object from the eud.engageUser function to the render_template call here
        return(render_template('marketStats.html',form=form,image_path=image_url,tradePrice=mkt_price))
    elif form.submit.data:
        session['tradetype']=form.tradeRadio.data
        #this version of the call will store the trade in the db
        eud.engageUser('a',ticker=session['trade_dict']['ticker'],qty=float(form.coinFreqString.data),tradetype=form.tradeRadio.data,confirmed=True)
        return(redirect('/main_menu'))
    return(render_template('tradeDeetsMenu.html', form=form))

@app.route('/coin_trade_history',methods=['GET','POST'])
def renderHistory():
    return
    
@app.route('/trade_blotter', methods = ['GET'])
def renderBlotter():
    table=eud.engageUser('b')
    return(render_template('trade_blotter.html', html_table=table))