
import os
import re

from selenium import webdriver
import time
import pandas as pd
from datetime import date
import numpy as np
import re
import codecs
import matplotlib as plt

userid = 'gerard.mazi@gmail.com'
password = 'rakutenisnumerouno'

# Download updated chromedriver and extract zip into the Downloads directory
# Open terminal and navigate to Downloads directory as cd /Users/gerardmazi/Downloads/
# Remove chromedriver from quarantine with xattr -d com.apple.quarantine chromedriver

chromedriver = '/Users/gerardmazi/Downloads/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()
driver.get('https://www.rakuten.com/')
time.sleep(2)

# Log in
#driver.find_element_by_xpath('//*[@class="css-1rydq7m"]').click()
#time.sleep(1)
#driver.find_element_by_xpath('//*[@name="username"]').send_keys(userid)
#time.sleep(1)
#driver.find_element_by_xpath('//*[@name="password"]').send_keys(password)
#time.sleep(1)
#driver.find_element_by_xpath('//*[@class="eb-auth-btn eb-auth-hover-btn eb-si-btn"]').click()
#time.sleep(1)

# Go to list of retailers
driver.get('https://www.rakuten.com/stores/all/index.htm')

# Store names
store = driver.find_elements_by_xpath('//span[@class="store-name blk"]')
store_temp = []
for s in store:
    store_temp.append(s.text)

# Store coupon
coupon = driver.find_elements_by_xpath('//span[@class="store-rebate blk cb"]')
coupon_temp = []
for c in coupon:
    if re.findall(r'%', c.text) == ['%']:
        coupon_temp.append(float(re.findall(r'\d+\.\d+', c.text)[0])/100)
    elif re.findall(r'%', c.text) == ['%', '%']:
        coupon_temp.append(float(re.findall(r'\d+\.\d+', c.text)[0])/100)
    elif re.findall(r'\$', c.text) == ['$']:
        coupon_temp.append(float(re.findall(r'\d+\.\d+', c.text)[0]))
    elif re.findall(r'\$', c.text) == ['$', '$']:
        coupon_temp.append(float(re.findall(r'\d+\.\d+', c.text)[0]))
    else:
        coupon_temp.append(float('nan'))

# Get list of sites with discount info
retailer = driver.find_elements_by_xpath('//*[@class="store-sort"]/li/div/a')
retailer_temp = []
for r in retailer:
    retailer_temp.append(r.get_attribute('href')[24:])

# Aggregate
disc_temp = pd.DataFrame(
    {
        'Date': pd.to_datetime(date.today()),
        'Source': 'Rakuten',
        'Merchant': store_temp,
        'Site': retailer_temp,
        'Discount': coupon_temp
    }
)

# Store
disco = pd.read_pickle('Discount/disco.pkl')
disco = pd.concat([disc_temp, disco], ignore_index=True)
disco.to_pickle('Discount/disco.pkl')

########################################################################################################################
# Analytics
disco[disco.Discount < 1].groupby(['Date'])['Discount'].mean()
disco[disco.Discount < 1].groupby(['Merchant', 'Date'])['Discount'].mean().unstack()
disco[(disco.Discount < 1) & (disco.Merchant == '1-800 CONTACTS')]
