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
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
sys.setrecursionlimit(10000)


#Setting options for webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

URL = "https://www.carrefoursa.com/tr/"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()
driver.get(URL)

#This is for category list. We need to acces this first.
categoryList = driver.find_element_by_xpath("//*[@id='category-1']")

try:
    
    #We can access each of these elements on category list.
    all_children_by_xpath = categoryList.find_elements_by_xpath("//*[@id='category-1']/li[]")
    
    #We are clicking two times because otherwise element is just selected because of structure of WebElement
    sleep(2)
    ##all_children_by_xpath.click()
    ##all_children_by_xpath.click()
    
    href_alincak = all_children_by_xpath.find_elements_by_css_selector("*")
    for i in range(0,len(all_children_by_xpath)):
        print(href_alincak[i].get_attribute("href"))
    
except StaleElementReferenceException:
    print("EEEEEEEEEEEEee")
    


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
    
    
curDF = parsePage(URL)
    
    
    
    
    
    
    
    
    
    
    
    
#Writing data to csv
#carrefour_df.to_csv('CarrefourSA_product_list.csv')

      
   


