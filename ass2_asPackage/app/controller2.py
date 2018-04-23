#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controller class to the equity trading platform
"""

import sys

from flask import Flask

sys.path.append('/home/lechuza/Documents/CUNY/data_607/flask_work/ass2_production-master/library')
#sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/ass1_fromWork')
sys.path.append('/usr/src/app/PROJECT_FOLDER')
#import engageUser as eu
import testing

app = Flask(__name__)

@app.route("/")
def main():
    ''' building console interaction '''
    #uncomment these when ready to handle web forms
    #engage=eu.Dialogue()
    #engage.engageUser()
    return(testing.run())

