# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
@author: Yasin Bursali, 5 Aug 2019
This application pulls name and price data of products from a e-commercial site named carrefour and puts it in pandas dataframe. Then it saves data as csv file.
"""

import bs4
import requests
from selenium import webdriver
import sys   
import pandas as pd
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
sys.setrecursionlimit(10000)


#Setting options for webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

currentURL = "https://www.carrefoursa.com/tr/katalog-urunleri/c/9001"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()

#Initializing pandas dataframe for price and product name
carrefour_df = pd.DataFrame({'Name' : [], 'Price' : []})

while(True):
    
    driver.get(currentURL)
    
    try:
        #Getting data for each page
        r = requests.get(currentURL)
        soup = bs4.BeautifulSoup(r.text,"xml")

        #Defining parse functions. These functions are taking indexes for finding all elements for giving order. 
        #They return data that pulled from site as string.
        def parseName(index):
        
            name = soup.find_all('span',{'class':'item-name'})[index].text
            return name

        def parsePrice(index):
    
            price = soup.find_all('span',{'class':'item-price'})[index].text
            return price

        for i in range(len(soup.find_all('span',{'class':'item-name'}))):
            carrefour_df = carrefour_df.append({'Name' : parseName(i), 'Price' : parsePrice(i)},ignore_index=True)
        
        #Clicking button to navigate next page
        button = driver.find_element_by_xpath("//a[@class='pr-next']")
        sleep(1.5)
        button.click()
        currentURL = driver.current_url
        
    except NoSuchElementException:
        break
    
#Writing data to csv
carrefour_df.to_csv('CarrefourSA_product_list.csv')

      
   


