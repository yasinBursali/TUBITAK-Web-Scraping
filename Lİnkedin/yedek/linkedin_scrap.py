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

sys.setrecursionlimit(10000)


          
      
    
#Setting options for webdriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-notifications")

URL = "https://www.linkedin.com"
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
driver.maximize_window()
driver.get(URL)



#Taking all links trough pages. it includes clicking and parsing links
links = []
j=0
nextURL = "https://www.linkedin.com/jobs/search/?sortBy=DD&start=0"
driver.get(nextURL)
while(j!=5):
    hrefList = driver.find_elements_by_xpath("//a[@data-control-name='A_jobssearch_job_result_click']")

    for i in range(len(hrefList)):
        link = hrefList[i].get_attribute("href")
        if link not in links:
            links.append(link)
    nextURL = "https://www.linkedin.com/jobs/search/?sortBy=DD&start=" + str((j+1)*25)
    
    driver.get(nextURL)
    sleep(0.5)
    j+=1 
    
        





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
    i=0
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
    



#Initializing dataframe for keeping data
dataframeJobs = pd.DataFrame({'Job Title' : [],'Company Name' : [],'Company Location' : [],'Skills' : [],'Seniority Level' : [],'Industry' : [],'Employment Type' : [],'Job Functions' : [],},index=None)


for i in range(len(links)):
    nextURL = links[i]
    driver.get(nextURL)
    sleep(0.5)
    #Clicking see more button. Otherwise bot cannot see features
    buttonSeeMore = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--2 artdeco-button--tertiary ember-view']")
    buttonSeeMore.click()
    #Check if the announcment has a required skills section. If there is, take that listing to dataframe
    skill = driver.find_elements_by_xpath("//h4[@class='t-14 t-black t-bold mb1']")
    if(len(skill) != 0):  
        dataframeJobs = dataframeJobs.append({'Job Title' : parseJob(),'Company Name' : parseCompanyName(),'Company Location' : parseCompanyLocation(),'Skills' : parseSkills(),'Seniority Level' : parseSeniorityLevel(),'Industry' : parseIndustry(),'Employment Type' : parseEmploymentType(),'Job Functions' : parseFunctions()},ignore_index=True)


       
        


dataframeJobs.to_csv('output.csv',index=False)

    
    
    
      
   


