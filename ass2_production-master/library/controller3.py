#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 10:17:25 2018

@author: lechuza
"""

import sys
sys.path.append('/home/lechuza/Documents/CUNY/data_607/flask_work/ass2_production-master/library')
#sys.path.append('/home/tio/Documents/CUNY/advancedProgramming/ass1_fromWork')
sys.path.append('/usr/src/app/PROJECT_FOLDER')
import testing

def main():
    ''' building console interaction '''
    testing.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()