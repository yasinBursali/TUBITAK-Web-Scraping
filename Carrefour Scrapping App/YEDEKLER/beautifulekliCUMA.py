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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
sys.setrecursionlimit(10000)



def parsePage(currentURL):
    
    page_df = pd.DataFrame({'Name' : [], 'Price' : [],'Category' : []})

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
            sleep(1.5)
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

URL = "https://www.carrefoursa.com/tr/"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()
driver.get(URL)


#This is for category list. We need to acces this first.
categoryList = driver.find_element_by_xpath("//*[@id='category-1']")


#xpath = "//*[@id='category-1']/li[%d]" % i
#all_children_by_xpath = categoryList.find_element_by_xpath(xpath)

links = []
href_alincak = categoryList.find_elements_by_xpath("//li//a[@class='']")



for i in range(len(href_alincak)):
    links.append(href_alincak[i].get_attribute("href"))
    

dataframeList = pd.DataFrame({'Dataframe' : []})
dataframes = []
for i in range(len(links)):
    driver.get(links[i+4])
    dataframeList = dataframeList.append({'Dataframe' : parsePage(links[i+4])},ignore_index=True)
   # dataframes.append = parsePage(URL)

    
    
    
    
#DRIVER AÇIP TEKER TEKER KATEGORI AÇMA DENEMESİ
#drivers = [None] * 12
#
#
#
#for i in range(1,12):
#    
#    if(i==1):
#        continue
#    else:
#        drivers[i] = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
#        drivers[i].maximize_window()
#        drivers[i].get(URL)
#        categoryList = driver.find_element_by_xpath("//*[@id='category-1']")
#        href_alincak = categoryList.find_elements_by_xpath("//li//a[@class='']")
#
#
#    
#    #We can access each of these elements on category list.
#    xpath = "//*[@id='category-1']/li[%d]" % i
#    all_children_by_xpath = categoryList.find_element_by_xpath(xpath)
#       
#    #We are clicking two times because otherwise element is just selected because of structure of WebElement
#    sleep(2)
#    all_children_by_xpath.click()
#    all_children_by_xpath.click()
#        
#    if(i==1):
#        sleep(1.5)
#        driver.quit()
#    else:    
#        sleep(1.5)
#        drivers[i].quit()
#    
#    




    
    
    
    
    
    
    
    
    
    
#Writing data to csv
#carrefour_df.to_csv('CarrefourSA_product_list.csv')

      
   


