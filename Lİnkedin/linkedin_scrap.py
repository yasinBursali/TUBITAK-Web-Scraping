# -*- coding: utf-8 -*-
"""
@author: Yasin Bursali, 5 Aug 2019
This application pulls name and price data of products from a e-commercial site named carrefour and puts it in pandas dataframe. Then it saves data as csv file.
"""
import pandas as pd
from selenium import webdriver
import sys   
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

sys.setrecursionlimit(10000)


          
#Setting options for webdriver
def setWebdriver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("–proxy-server=78.157.215.87:3128")
    
    URL = "https://www.linkedin.com/"
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(URL)
    return driver

#Automatic login
def autoLogin(driver):
    sleep(0.5)
    driver.find_element_by_xpath("//input[@name='session_key']").send_keys("sxvse2r0@iffymedia.com")
    driver.find_element_by_xpath("//input[@name='session_password']").send_keys("1234qweR")
    driver.find_element_by_xpath("//button[@data-tracking-control-name='guest_homepage-basic_sign-in-submit-btn']").click()


#Taking all listed job's links trough pages. it includes clicking and parsing links.
#Parses 40 pages because Linkedin only shows up to 40 pages per search.
def parseLinks():
    #City URLS are have been choosen manually because selenium's bugs and lack of time
    cities = ["https://www.linkedin.com/jobs/search/?geoId=102240587&location=Alabama%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=100290991&location=Alaska%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=106032500&location=Arizona%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=102790221&location=Arkansas%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=102095887&location=California%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=105763813&location=Colorado%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=106914527&location=Connecticut%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=105375497&location=Delaware%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=101318387&location=Florida%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=106315325&location=Georgia",
              "https://www.linkedin.com/jobs/search/?geoId=103977389&location=Washington%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=104453637&location=Vermont%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=101630962&location=Virginia%2C%20United%20States","https://www.linkedin.com/jobs/search/?geoId=104454774&location=Wisconsin%2C%20United%20States",
              "https://www.linkedin.com/jobs/search/?geoId=102257491&location=London%2C%20England%2C%20United%20Kingdom","https://www.linkedin.com/jobs/search/?geoId=101098412&location=Massachusetts%2C%20United%20States"]
    links = []
    nextURL = "https://www.linkedin.com/jobs/"
    driver.get(nextURL)
    
    pageMax=40
    pageCount=0
    for j in cities:
    
        driver.get(j)
        pageMax=40                                    
        pageCount=0    
        while(pageCount!=pageMax):
            nextURL = j
            hrefList = driver.find_elements_by_xpath("//a[@data-control-name='A_jobssearch_job_result_click']")
            for i in range(len(hrefList)):
                link = hrefList[i].get_attribute("href")
                if link not in links:
                    print("Taking links in" + str(pageCount) + ". page")
                    links.append(link)
            
            nextURL = nextURL[:len(j)]
            nextURL = nextURL + "&start=" +str((pageCount+1)*25)
            sleep(2)
            driver.get(nextURL)
            sleep(2)
            pageCount+=1 
    
        
            
    return links

                                        
def parseJob():
    jobTitle = driver.find_element_by_xpath("//h1[@class='jobs-top-card__job-title t-24']").text
    return jobTitle

def parseCompanyName():
    try:
        companyName = driver.find_element_by_xpath("//a[@class='jobs-top-card__company-url ember-view']").text
        return companyName

    except NoSuchElementException:
        return "N/A"
    
def parseCompanyLocation():
    try:
        location = driver.find_element_by_xpath("//span[@class='jobs-top-card__bullet']").text
        return location

    except NoSuchElementException:
        return "N/A"
    
  
def parseSkills():  
    returnText=""
    skills = driver.find_elements_by_xpath("//span[@class='jobs-ppc-criteria__value t-14 t-black t-normal ml2 block']")
    for i in range(len(skills)):
        if i==(len(skills)-1):
            returnText += skills[i].text
        else:
           returnText += skills[i].text + ","
    return returnText

def parseSeniorityLevel():
    try:
        seniorityLevel = driver.find_element_by_xpath("//p[@class='jobs-box__body js-formatted-exp-body']").text
        return seniorityLevel

    except NoSuchElementException:
        return "N/A"

def parseIndustry():
    
    
    returnText=""
    try:
        industry = driver.find_elements_by_xpath("//li[@class='jobs-box__list-item jobs-description-details__list-item']")
        for i in range(len(industry)):
            if i==(len(industry)-1):
                returnText += industry[i].text
            else:
                returnText += industry[i].text + ","
        return returnText

    except NoSuchElementException:
        return "N/A"

def parseEmploymentType():
    returnText=""
    try:
        employmentType = driver.find_elements_by_xpath("//p[@class='jobs-box__body js-formatted-employment-status-body']")
        for i in range(len(employmentType)):
            if i==(len(employmentType)-1):
                returnText += employmentType[i].text
            else:
                returnText += employmentType[i].text + ","
        return returnText

    except NoSuchElementException:
        return "N/A"

def parseFunctions():
    try:
        jobFunctions = driver.find_element_by_xpath("//ul[@class='jobs-box__list jobs-description-details__list js-formatted-job-functions-list']").text
        return jobFunctions

    except NoSuchElementException:
        return "N/A"
    

driver = setWebdriver()
autoLogin(driver)
links = parseLinks()
#Initializing dataframe for keeping data
dataframeJobs = pd.DataFrame({'Job Title' : [],'Company Name' : [],'Company Location' : [],'Skills' : [],'Seniority Level' : [],'Industry' : [],'Employment Type' : [],'Job Functions' : [],},index=None)
#links = pd.read_csv('links.csv') if links are in csv file
    
for i in range(0,5908):
    nextURL = links["0"][i]
    driver.get(nextURL)
    sleep(1.8)
      #Check if the announcment has a required skills section. If there is, take that listing to dataframe
    try:
        print("Appending " + str(i) + ". page")
        dataframeJobs = dataframeJobs.append({'Job Title' : parseJob(),'Company Name' : parseCompanyName(),'Company Location' : parseCompanyLocation(),'Skills' : parseSkills(),'Seniority Level' : parseSeniorityLevel(),'Industry' : parseIndustry(),'Employment Type' : parseEmploymentType(),'Job Functions' : parseFunctions()},ignore_index=True)
        dataframeJobs.to_csv('OutputFile.csv',index=False)
        
    except (NoSuchElementException,StaleElementReferenceException):
        continue

       
        



    
    
#links_df = pd.DataFrame(links)
#links_df=links_df.to_csv('links.csv',index=False)

    
      
   


