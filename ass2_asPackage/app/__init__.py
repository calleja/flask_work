from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

#recursive
from app import testing
import os

#'app' is actually a global variable inside of _01_simple.py... app is an instantiation of a Flask object from the basic Flask module - as opposed to a customized one

''' legacy code to implement later
from library.controller2 import app

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port) #spins up a server and waits for request from client

'''
