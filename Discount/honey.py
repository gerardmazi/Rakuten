
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


# Download updated chromedriver and extract zip into the Downloads directory
# Open terminal and navigate to Downloads directory as cd /Users/gerardmazi/Downloads/
# Remove chromedriver from quarantine with xattr -d com.apple.quarantine chromedriver

chromedriver = '/Users/gerardmazi/Downloads/chromedriver'
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()
driver.get('https://capitaloneshopping.com/s/all')
time.sleep(2)

# Store names
store = driver.find_elements_by_xpath('//*[@class="charcoal"]')
store_temp = []
for s in store:
    store_temp.append(s.text)

# Get list of sites with discount info
retailer = driver.find_elements_by_xpath('//*[@class="site-column"]/a')
retailer_temp = []
for r in retailer:
    retailer_temp.append(r.get_attribute('href'))

# Navigate to retailers page for discount
coupon_temp = []

for rit in retailer_temp:

    # Get the coupon
    try:
        driver.get(rit)

        try:
            coupon_temp.append(
                driver.find_element_by_xpath('//*[@class="overview-card-bottom"]/div[3]/span[2]').text
            )
        except:
            try:
                coupon_temp.append(
                    driver.find_element_by_xpath('//*[@class="overview-card-bottom"]/div[2]/span[2]').text
                )
            except:
                try:
                    coupon_temp.append(
                        driver.find_element_by_xpath('//*[@class="overview-card-bottom"]/div[1]/span[2]').text
                    )
                except:
                    coupon_temp.append('nan')

    except:
        coupon_temp.append('nan')

    time.sleep(1)

# Cleanup coupon_temp
#coupon_temp_temp = []
#for i in coupon_temp:
#    if re.findall(r'%', i) == ['%']:
#        coupon_temp_temp.append(float(re.findall(r'\d+\.\d+', i)[0])/100)
#    elif re.findall(r'\$', i) == ['$']:
#        coupon_temp_temp.append(re.findall(r'\d+\.\d+', i)[0])
#    else:
#        coupon_temp_temp.append(float('nan'))

#coupon_temp_temp = []
#for i in coupon_temp:
#    if re.findall(r'%', i) == ['%']:
#        coupon_temp_temp.append(float(re.findall(r'\d+\.\d+', i)[0])/100)
#    elif re.findall(r'\$', i) == ['$']:
#        coupon_temp_temp.append(re.findall(r'\d+\.\d+', i)[0])
#    else:
#        coupon_temp_temp.append(float('nan'))

#[re.findall(r'%', i) for i in capone_temp['Discount']]


# Aggregate
capone_temp = pd.DataFrame(
    {
        'Date': pd.to_datetime(date.today()),
        'Source': 'CapitalOne',
        'Merchant': store_temp,
        'Site': retailer_temp,
        'Discount': coupon_temp
    }
)

# Store
capone = pd.read_pickle('Discount/capone.pkl')
capone = pd.concat([capone, capone_temp], ignore_index=True)
capone.to_pickle('Discount/capone.pkl')