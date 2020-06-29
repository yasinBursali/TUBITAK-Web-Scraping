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


#Setting options for webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")

URL = "https://www.carrefoursa.com/tr/"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()
driver.get(URL)



r = requests.get(URL)
soup = bs4.BeautifulSoup(r.text,"xml")

categoryList_soup = soup.find_all('ul',{'id':'category-1'})[0]
categoryList_sp = soup.select('#category-1')



links_soup = []

hrefPuller = categoryList_sp.find_all('a',{'class':''},recursive=True)

for i in range(1,len(hrefPuller)):
    
    links_soup.append(hrefPuller[i].get('href'))
    print (hrefPuller[i].get('href')) ##BURASI BÜTÜN ÜRÜNLERİ DÖNDÜRDÜ

for i in range(1,len(hrefPuller)):
     
    child_hrefPuller = hrefPuller[i].find_all('a',{'class':''})


#This is for category list. We need to acces this first.
categoryList = driver.find_element_by_xpath("//*[@id='category-1']")

#
#xpath = "//*[@id='category-1']/li[%d]" % i
#all_children_by_xpath = categoryList.find_element_by_xpath(xpath)

links = []
href_alincak = categoryList.find_elements_by_xpath("//li//a[@class='']")



for i in range(len(href_alincak)):
    links.append(href_alincak[i].get_attribute("href"))

for i in range(1,12):
    try:
        try:
            #We can access each of these elements on category list.
            xpath = "//*[@id='category-1']/li[%d]" % 5

            all_children_by_xpath = categoryList.find_element_by_xpath(xpath)
#
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
            all_children_by_xpath = WebDriverWait(categoryList, 10,ignored_exceptions=ignored_exceptions)\
                       .until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
                      

            
           
                    
        
        except NoSuchElementException:
            print("ERROR:NO SUCH ELEMENT ")
        
    
            #We are clicking two times because otherwise element is just selected because of structure of WebElement
            sleep(2)
            all_children_by_xpath.click()
            all_children_by_xpath.click()
        
        
    except StaleElementReferenceException:
        print("ERROR:STALE ELEMENT REF")
        break
    
    sleep(1)
    driver.get(URL)
    #driver.execute_script("window.history.go(-1)")
    
    





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

      
   


