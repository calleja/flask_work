#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 10:02:36 2018

@author: lechuza
"""
from app import app #we're only told that the second "app" reference here is a variable... it may be a global variable!
from flask import render_template

@app.route("/")
@app.route("/index")
def run():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    
    return(render_template('index.html',title='Home',user=user,posts=posts))
    #return(html)
