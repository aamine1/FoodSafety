import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import time
from selenium.webdriver.common.action_chains import ActionChains
import random
import xlrd

    
file_location = "path"
workbook=xlrd.open_workbook(file_location)
sheet=workbook.sheet_by_index(0)
L=[]
for r in range(sheet.nrows):
    L.append(sheet.cell_value(r,0))

chromedriver = "path"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
actions=ActionChains(driver)
driver.implicitly_wait(5)

time.sleep(random.uniform(0,2))

# Sign in using username and password
# Username
driver.get("http://www.importgenius.com")


driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/a[2]').click()


time.sleep(random.uniform(0,2))
driver.find_element_by_xpath('//*[@id="username"]').click()
driver.switch_to.active_element.send_keys("aanoun@mit.edu")

time.sleep(random.uniform(0,2))

driver.switch_to.active_element.send_keys(Keys.TAB)
driver.switch_to.active_element.send_keys("password")

driver.switch_to.active_element.send_keys(Keys.RETURN)


driver.find_element_by_xpath('//*[@id="conditions"]/div/select[2]').click()

driver.find_element_by_xpath('//*[@id="conditions"]/div/select[2]/option[2]').click()

driver.find_element_by_xpath('//*[@id="conditions"]/div/span[1]/input').click()

driver.switch_to.active_element.send_keys(L[1])

driver.find_element_by_xpath('//*[@id="conditions"]/div/input[1]').click()

driver.find_element_by_xpath('//*[@id="conditions"]/div[2]/select[1]').click()

driver.find_element_by_xpath('//*[@id="conditions"]/div[2]/select[1]/option[2]').click()

for i in range(2,len(L)-1):
    
    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/select[2]').click()

    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/select[2]/option[2]').click()

    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/span[1]/input').click()

    #time.sleep(1)

    driver.switch_to.active_element.send_keys(L[i+1])

    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/input[1]').click()

    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/select[1]').click()

    #time.sleep(1)

    driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i)+']/select[1]/option[2]').click()


driver.find_element_by_xpath('//*[@id="conditions"]/div['+str(i+1)+']/input[2]').click()

driver.find_element_by_xpath('//*[@id="filtertable"]/tbody/tr/td/form/div[1]/div[1]/div/button[1]/span/b').click()




