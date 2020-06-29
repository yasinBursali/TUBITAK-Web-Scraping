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
from time import gmtime, strftime
import os
sys.setrecursionlimit(10000)



#Takes page URL as paramater, parses page and clickes next button. Finally returns pandas dataframe. 
def parsePage(currentURL):
    
    page_df = pd.DataFrame({'Name' : [], 'Price' : [],'Category' : []},index=None)

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
            
            def parseCategory(index):
                
                category = soup.select('input[name=productMainCategoryPost]')[index]['value']
                return category
            
            for i in range(len(soup.find_all('span',{'class':'item-name'}))):
                page_df = page_df.append({'Name' : parseName(i), 'Price' : parsePrice(i),'Category' : parseCategory(i)},ignore_index=True)
                
            #Clicking button to navigate next page
            button = driver.find_element_by_xpath("//a[@class='pr-next']")
            #If your internet connection is not fast enough, you can increase sleep's argument
            sleep(0.5)
            button.click()
            #For remembering last url
            currentURL = driver.current_url
                
        except NoSuchElementException:
            break
        
    return page_df
    
    
#Setting options for webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")

URL = "https://www.carrefoursa.com/tr/meyve-sebze/c/1014"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()
driver.get(URL)


#This is for category list. We need to acces this first.
categoryList = driver.find_element_by_xpath("//*[@id='category-1']")

links = []
href_alincak = categoryList.find_elements_by_xpath("//li//a[@class='']")


for i in range(len(href_alincak)):
    links.append(href_alincak[i].get_attribute("href"))
    

dataframeList = pd.DataFrame({'Dataframe' : []},index=None)

for i in range(2,len(links)):
    driver.get(links[i])
    dataframeList = dataframeList.append({'Dataframe' : parsePage(links[i])},ignore_index=True)



#Creatiing a directory and writing data to csv. Csv saved in "Output_" + currentTime folder
currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
os.mkdir("Output_" + currentTime)
dirPATH = "/home/yasin/Desktop/Carrefour Scrapping App" + "Output_" + currentTime
for j in range(0,len(dataframeList)):
    df_temp = dataframeList['Dataframe'][j]
    if(len(df_temp) > 110):
        df_temp = dataframeList['Dataframe'][j]
        df_temp.to_csv(dirPATH,currentTime + '_CarrefourSA_product_list_' + df_temp["Category"][0] + '.csv',index=False)
    



    
    
    
    
      
   


