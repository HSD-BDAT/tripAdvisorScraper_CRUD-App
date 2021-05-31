#!/usr/bin/env python
# coding: utf-8
# 2021-05-30
#%%
# import required packages
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.common.by import By     
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time
from datetime import datetime

#%%
# list of Websites to find individual links for tripAdvisor pages
# each of these weblinks contains 30 attractions
webLinks = ['https://www.tripadvisor.in/Attractions-g155019-Activities-a_allAttractions.true-Toronto_Ontario.html',
            'https://www.tripadvisor.in/Attractions-g155019-Activities-oa30-Toronto_Ontario.html',
            'https://www.tripadvisor.in/Attractions-g155019-Activities-oa60-Toronto_Ontario.html',
            'https://www.tripadvisor.in/Attractions-g155019-Activities-oa90-Toronto_Ontario.html',
            'https://www.tripadvisor.in/Attractions-g155019-Activities-oa120-Toronto_Ontario.html']
print(webLinks)

#%%
# iterate over Main links
for weblink in webLinks:
    print(weblink)
    page = requests.get(weblink)
    
    # Connect with MongoDB Atlas
    client = MongoClient("mongodb+srv://bdatAdmin:HCjquZSkonIiojmi@cluster0.zbfiq.mongodb.net/trip?retryWrites=true&w=majority")
    
    # create a Database/Collection named 'socialMining_01'
    db = client.socialMining_01
    
    #%%
    # load the main site and get the attractions hyperlinks
    soup = BeautifulSoup(page.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href = True):
        links = links + [a['href']]
    
    #%%
    # we are only interested in attraction site hrefs 
    index_element = [i for i in ["Attraction_Review" in x for x in links]] 
    
    #%%
    path = [a for a in list(set([links[i] for i in list(np.where(index_element)[0])])) 
            if a.startswith('/Attraction_Review') & a.endswith('html')]
    
    #%%
    # using Selenium with Microsoft Edge driver to read the dynamic content of the websites
    # In the beautifulSoup html, `website`, `Phone`, `Email` links are not accessible
    # using Selenium, we first load the webpage and wait for the dynamic content to be loaded.
    driver = webdriver.Edge(executable_path  = 'C:/Users/007/Desktop/msedgedriver.exe')
    
    #%%
    for i in range(0,len(path)):
        print(i)
        relativePath = path[i]
        # path to individual attraction site
        absPath = 'https://www.tripadvisor.in' + relativePath
    ######################################################################
    # Selenium part
    # this loads the website in edge
        driver.get(absPath)
        # we wait for 15 seconds to let the website load completely
        time.sleep(15)
        
        # we further allow 20 seconds implicity to find our elements
        try:
            elems = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uB5OQXin > a"))) #div.uB5OQXin > a
            contactInfo = [elem.get_attribute('href') for elem in elems]
            print(contactInfo)
        except: contactInfo = []
    # Selenium ends    
    ######################################################################
    # from here onwards only beautifulSoup is used
        page = requests.get(absPath)
        soup = BeautifulSoup(page.text, 'html.parser')
        
    ######################################################################
    # to get elements exception handling is used, if element is missing or any other error
    # we get empty value for the element
    # Data cleaning is done after getting the element and before uploading data to mongoDB
        dict1 = dict()
        ################### using Selenium results
        try:
            dict1['Website'] = [a for a in contactInfo if a.startswith('http')][0]
        except: dict1['Website'] = ''
            
        try:
            dict1['Phone'] = [a for a in contactInfo if a.startswith('tel')][0]
            dict1['Phone'] = '+1-' + re.sub('tel:%2B1%20', '', dict1['Phone'])
        except: dict1['Phone'] = ''
            
        try:
            dict1['Email'] = [a for a in contactInfo if a.startswith('mailto')][0]
            dict1['Email'] = re.sub('mailto:', '', dict1['Email'])
        except: dict1['Email'] = ''
        ###################
        try:
            dict1['Rating'] = soup.find('div', class_='DrjyGw-P _1SRa-qNz _3t0zrF_f _1QGef_ZJ').contents[0]
            dict1['Rating'] = float(re.sub(',', '', dict1['Rating']))
        except: dict1['Rating'] = ''
            
        try:
            dict1['# of Reviews'] = soup.find('span', class_='DrjyGw-P _26S7gyB4 _14_buatE _2nPM5Opx').contents[0].get_text()
            dict1['# of Reviews'] = int(re.sub(',', '', dict1['# of Reviews']))
        except: dict1['# of Reviews'] = ''  
            
        # perfect reviews % is calculated by dividing Excellent Reviews/Total Reviews
        try:
            dict1['Perfect Reviews %'] = round(100 * int(re.sub(',', '', soup.find('div', class_ = 'DrjyGw-P _26S7gyB4 _1dimhEoy').get_text()))/dict1['# of Reviews'])
        except: dict1['Perfect Reviews %'] = ''
            
        try:
            dict1['Address'] = soup.find('button', class_='LgQbZEQC _1v-QphLm _1fKqJFvt').contents[0].get_text()
        except: dict1['Address'] = ''
            
        try:
            dict1['Suggested Duration'] = soup.find('div', class_='_1-hfw1lg').contents[0]
        except: dict1['Suggested Duration'] = '' 
            
        try:
            dict1['Name'] = soup.find('h1', class_="DrjyGw-P _1SRa-qNz qf3QTY0F").contents[0]
        except: dict1['Name'] = '' 
            
        try:
            dict1['Rank'] = soup.find('a', class_="LgQbZEQC _1v-QphLm _1fKqJFvt").contents[0].get_text()
            dict1['Rank'] = int(dict1['Rank'].split(' ', 1)[0].replace('#', ''))            
        except: dict1['Rank'] = '' 
            
        try:
            dict1['Timings'] = soup.find('div', class_="nGgs_vBt").contents[0].find('span', class_='_15_skC_h').get_text()
        except: dict1['Timings'] = '' 
            
        try:
            dict1['Open'] = soup.find('div', class_="nGgs_vBt").contents[0].find('span', class_='DrjyGw-P _1l3JzGX1').get_text()
        except: dict1['Open'] = ''
            
        try:
            dict1['Neighbourhood'] = soup.find('div', class_='_276-4yo8').contents[0].get_text().split(': ')[1]
        except: dict1['Neighbourhood'] = ''
            
        try:
            dict1['Summary'] = soup.find('div', class_="cPQsENeY u7nvAeyZ").contents[0].get_text()
        except: dict1['Summary'] = ''
        
        dict1['_id'] = dict1['Name']
        try:
            dict1['Group'] = soup.find_all('div', class_='_28X3NMFC')[2].text
            dict1['Group'] = re.sub('([^a-zA-Z0-9&, _]|^\s)', '|', dict1['Group'])
        except: dict1['Group'] = ''
        
        dict1['Link'] = absPath
        dict1['timeScraped'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    ######################################################################
    # Add the scraped data to mongoDB table `scraped` under our database
        try:
            db.scraped.insert_one(dict1)
        except: ''    
        
        #%%
# for confirmation if data is properly scraped or not        
obs = db.scraped.find()
a = pd.DataFrame([ob for ob in obs])
        