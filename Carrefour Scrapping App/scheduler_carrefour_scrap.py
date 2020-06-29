#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:13:17 2019

@author: Yasin Bursali
        
"""
import schedule
import time
from subprocess import call


def call_script():
    call(["python", "carrefour_scrap.py"])
    
schedule.every().monday.at("15:27").do(call_script)

while 1:
    schedule.run_pending()
    time.sleep(1)