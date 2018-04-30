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
from app import retrieveMarkets

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
        return(redirect('/main_menu'))
	#handle the rendering 
    return(render_template('main_menu_crypt.html', title='Main Menu', form=form))
	
index_start=0
    
@app.route('/crypto_menu',methods=['GET','POST'])
def cryptoMenu():
    rm=retrieveMarkets.RetrieveMarkets()
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
            flash('running this {}, baby'.format(request.method))
            flash('que pinga numero {}'.format(session['number']))
            session['number'] +=1
            g=session['number']*increment
            subsection=session['cryptos'][g:g+increment]
            return(render_template('index_crypt.html', title='Main Menu', menu=subsection, form=cform))
    
    #first rendering with a GET request
    flash('running this {}'.format(request.method))
    return(render_template('index_crypt.html', title='Main Menu', menu=subsection, form=cform))
    
    
    '''
def subsection():
    g=g+increment
    
        if user_input=='n':
            while user_input=='n' and   g<df.shape[0]+(increment-2):
                print(df.loc[:,['Currency','CurrencyLong']].iloc[g:g+increment])
                g=g+increment
                user_input=input('> ')
            #TODO user_input ne 'n' breaks the loop, must then evaluate the user input
    '''
            
            
