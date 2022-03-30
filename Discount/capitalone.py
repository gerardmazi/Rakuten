
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

# Navgate to retailers page for discount
coupon_temp = []

for i in range(1, len(driver.find_elements_by_xpath('//*[@class="site-columns"]/li'))):

    # Open browser
    chromedriver = '/Users/gerardmazi/Downloads/chromedriver'
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    driver.get('https://capitaloneshopping.com/s/all')
    time.sleep(1)

    # Start iterating through each column of data
    column = driver.find_elements_by_xpath('//*[@class="site-columns"]/li[' + str(i) + ']/a')
    column_temp = []
    for c in column:
        column_temp.append(c.get_attribute('href'))

    for col in column_temp:

        try:
            # Go to retailer s
            driver.get(col)

            # Get the coupon
            try:
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
        except:
            coupon_temp.append('nan')

        time.sleep(2)

    # Quit and re-launch webdriver
    driver.quit()
    time.sleep(1)
