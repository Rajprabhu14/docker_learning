# -*- coding: utf-8 -*-
import csv
import os.path
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pause
from datetime import date
import unittest, time, re

'''location of chromium driver'''
chrome_path = "K:/chromedriver_win32/chromedriver.exe"
#firefox_path = "K:/chromedriver_win32/geckodriver.exe"
class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.flag = True
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome(chrome_path)
        # self.driver = webdriver.Firefox(executable_path=firefox_path)
        # self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.recordCountList = [];

    def test_app_dynamics_job(self):
        dateL = date.today()
        # final date string
        dateString = "{0}/{1}/{2}".format(dateL.strftime('%m'), dateL.strftime('%d'), dateL.year)
        driver = self.driver

        driver.get("https://idp.rae.clareity.net/idp/Authn/UserPassword")
        driver.find_element_by_id("j_username").send_keys("emelnymi")
        driver.find_element_by_id("password").click()
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("century21m")
        driver.find_element_by_id("loginbtn").click()
        pause.milliseconds(5000)
        driver.find_element_by_id("search-nav").click()
        pause.milliseconds(1500)
        driver.find_element_by_link_text("RESIDENTIAL").click()
        pause.milliseconds(3000)
        tab = driver.find_element_by_id('tab1_1')
        iframe = tab.find_element_by_tag_name('iframe')
        driver.switch_to.frame(iframe)
        pause.milliseconds(1000)
        driver.find_element_by_id("nodeSpreadsheets").click()
        pause.milliseconds(1000)
        driver.find_element_by_link_text("IH2").click()
        pause.milliseconds(2000)
        driver.switch_to_default_content()
        pause.milliseconds(2000)
        first_iframe= driver.find_element_by_id('tab1_1_2')
        driver.switch_to.frame(first_iframe)
        # div = driver.find_element_by_id('tab1_2')
        # tab2 = div.find_element_by_id('tab1_2_2')
        # driver.switch_to.frame(tab2)
        tab3 = driver.find_element_by_id('ifSpreadsheet')
        driver.switch_to.frame(tab3)
        columns = driver.find_elements_by_tag_name('th')
        pause.milliseconds(3000)
        field_array = []
        for col in columns:
            div = col.get_attribute('innerText')
            print(div)
            field_array.append(div)

        with open('mls_data.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_array)
            writer.writeheader()

        # move to status
        '''ActionChains(driver).key_down(Keys.TAB).perform()
        ActionChains(driver).key_down(Keys.TAB).perform()
        pause.milliseconds(1000)
        # sold enter
        ActionChains(driver).send_keys("sol").perform()
        ActionChains(driver).key_down(Keys.DOWN).perform()
        ActionChains(driver).key_down(Keys.ENTER).perform()
        pause.milliseconds(1000)
        # withdrawn enter
        ActionChains(driver).send_keys("wi").perform()
        ActionChains(driver).key_down(Keys.DOWN).perform()
        ActionChains(driver).key_down(Keys.ENTER).perform()
        pause.milliseconds(1000)
        # terminated enter
        ActionChains(driver).send_keys("te").perform()
        ActionChains(driver).key_down(Keys.ENTER).perform()
        pause.milliseconds(1000)
        # Expired enter
        ActionChains(driver).send_keys("ex").perform()
        ActionChains(driver).key_down(Keys.ENTER).perform()
        pause.milliseconds(1000)
        # date table move
        ActionChains(driver).key_down(Keys.TAB).perform()
        pause.milliseconds(1000)
        ActionChains(driver).key_down(Keys.TAB).perform()
        pause.milliseconds(1000)
        ActionChains(driver).send_keys("01/01/2018").perform()
        pause.milliseconds(1000)
        ActionChains(driver).key_down(Keys.TAB).perform()
        ActionChains(driver).send_keys("01/07/2018").perform()
        # ActionChains(driver).send_keys(dateString).perform()
        # pause.milliseconds(3000)
        tab = driver.find_element_by_id('tab1_1')
        iframe = tab.find_element_by_tag_name('iframe')
        driver.switch_to.frame(iframe)
        pause.milliseconds(3000)
        # Total count
        record = driver.find_element_by_id('CountResult').get_attribute('value')
        self.totalRecords = int(record.replace(',', ''))
        self.recordCountList = self.maxValueRecord(self.totalRecords)

        driver.find_element_by_id('Search').click()

        pause.milliseconds(10000)
        driver.switch_to.default_content()
        pause.milliseconds(5000)
        iFrame = driver.find_element_by_id('tab1_1_2')
        pause.milliseconds(3000)
        driver.switch_to.frame(iFrame)
        pause.milliseconds(3000)
        # search for table inside the iframe
        ifSpreadsheet = driver.find_element_by_id('ifSpreadsheet')
        driver.switch_to.frame(ifSpreadsheet)
        grid = driver.find_element_by_id('grid')
        tr =  grid.find_elements_by_tag_name('tr')
        self.splitRow(tr)
        pause.milliseconds(1000)'''

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)
    # tr row
    def splitRow(self, rows):
        for i in range(1, len(rows)):
            tds = rows[i].find_elements_by_tag_name('td')
            self.readColumn(tds)
    # value field read
    def readColumn(self, columns):
         # self.valueFormat()
         self.col_val = {}
         self.col_name = [];
         # self.col_val[columns[0].get_attribute('aria-describedby')] = self.id_scrapped
         columnLength = len(columns)
         for i in range(0, columnLength):
             # unwanted column filter
             if(columns[i].get_attribute('aria-describedby') != "grid_LISTING_PICTURES__1") & \
                 (columns[i].get_attribute('aria-describedby') != "grid_cb") & \
                 (columns[i].get_attribute('aria-describedby') != "None") & \
                 (columns[i].get_attribute('aria-describedby') != "grid_display_id__1") & \
                 (columns[i].get_attribute('aria-describedby') != "grid_INTEGRATION__1"):
                    self.col_name.append(columns[i].get_attribute('aria-describedby'))
                    if columns[i].get_attribute('innerHTML') != "&nbsp;":
                        self.col_val[columns[i].get_attribute('aria-describedby')] = columns[i].get_attribute('innerHTML')
                    else:
                        self.col_val[columns[i].get_attribute('aria-describedby')] = None
         self.writeCurrentDateValue(self.col_val, self.col_name)

    #csv writing function
    def writeCurrentDateValue(self, value, column):
        self.lastScrapped = int(value['grid_rn'])
        print(self.lastScrapped)
        if self.lastScrapped in self.recordCountList:
            self.newMaxValue = self.recordCountList[self.recordCountList.index(value['grid_rn']) + 1]
        else:
            myArray = np.array(self.recordCountList)
            pos = (np.abs(myArray - self.lastScrapped)).argmin()
            self.newMaxValue =  myArray[pos]

        with open('scrapping.csv', 'a', newline='', encoding='utf8') as csvfile:
            writer1 = csv.DictWriter(csvfile, fieldnames=column)
            if self.flag:
                writer1.writeheader()
                self.flag = False
            writer1.writerow(value)

    # array of value update in table
    def maxValueRecord(self, maxValue):
        x = []
        for n in np.arange(0, maxValue, 250):
            x.append(n)
        return x

if __name__ == "__main__":
    unittest.main()
