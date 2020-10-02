# -*- coding: utf-8 -*-
import csv
import os
import pause
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.sl_no = 0
        self.flag = True
        self.createdHeader = True
        d = date.today()
        date_day =  '-'.join(str(x) for x in (d.month, d.day, d.year))
        self.current_date = "current_" + date_day + ".csv"
        self.current_date = date_day
        previous_date = d - timedelta(1)
        print(previous_date)
        self.file_name = 'mssrf_' + '-'.join(str(x) for x in (previous_date.month, previous_date.day, previous_date.year)) + '.csv'

        print(previous_date)
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome(chrome_path)
        # self.driver = webdriver.Firefox(executable_path=firefox_path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        try:
            driver = self.driver
            driver.get("http://tn.crp.mssrf.weathertrack.in/IndexUI.aspx")
            driver.find_element_by_id("txtUserName").clear()
            driver.find_element_by_id("txtUserName").send_keys("admin@mssrf.in")
            driver.find_element_by_id("txtPwd").clear()
            driver.find_element_by_id("txtPwd").send_keys("$we@trck##")
            driver.find_element_by_id("Go").click()
            pause.milliseconds(3000)
            try:
                driver.find_element_by_xpath('//*[@id="menu"]/ul/li[2]/a').click()
                self.select = Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ddlEntity"))
                select_station_code = Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ddlUnitID"))
                option = self.select.options
                station_name = self.valueGetter(option)
                station_code = self.valueGetter(select_station_code.options)
                for number in range(1, option.__len__()):
                    self.select.select_by_index(number)
                    self.station_name = station_name[number]
                    self.station_code = station_code[number]
                    self.driver.find_element_by_link_text("Last Day").click()
                    # selected_option = select.first_selected_option
                    # print(selected_option.text)
                    # self.station_name = option[number].text
                    self.write_header()
                    self.write_value()
                    self.driver.back()
                    self.select = Select(self.driver.find_element_by_id("ctl00_ContentPlaceHolder1_ctl00_ddlEntity"))
            except:
                driver.find_element_by_id("ctl00_ImageButton1").click()
        except:
            driver.find_element_by_id("ctl00_ImageButton1").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            self.driver.find_element_by_id("ctl00_ImageButton1").click()
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            self.driver.find_element_by_id("ctl00_ImageButton1").click()
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
        self.driver.find_element_by_id("ctl00_ImageButton1").click()
        self.assertEqual([], self.verificationErrors)

    def write_header(self):
        if self.createdHeader:
            self.header_list = ['sl_no']
            self.header_obj = {}
            header_div = self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_DynaicHeaderDiv')
            header_th = header_div.find_elements_by_class_name('th')
            for th in header_th:
                self.header_list.append(th.get_attribute('innerText'))
                self.header_obj[th.get_attribute('innerText')] = ''
            self.createdHeader = False

    def write_value(self):
        try:
            table_content = self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_DynamicWeatherDataDiv')
            w1 = self.driver.find_elements_by_class_name('w1')
            w2 = self.driver.find_elements_by_class_name('w2')
            w3 = self.driver.find_elements_by_class_name('w3')
            w4 = self.driver.find_elements_by_class_name('w4')
            w5 = self.driver.find_elements_by_class_name('w5')
            w6 = self.driver.find_elements_by_class_name('w6')
            w7 = self.driver.find_elements_by_class_name('w7')
            w8 = self.driver.find_elements_by_class_name('w8')
            w9 = self.driver.find_elements_by_class_name('w9')
            w11 = self.driver.find_elements_by_class_name('w11')

            for i in range(1,w1.__len__()):
                print(w1[i].text, w2[i].text, w3[i].text, w4[i].text,
                      w5[i].text, w6[i].text, w7[i].text, w8[i].text,
                      w9[i].text, w11[i].text)
                self.header_obj[self.header_list[1]] = w1[i].text
                self.header_obj[self.header_list[2]] = w2[i].text
                self.header_obj[self.header_list[3]] = w3[i].text
                self.header_obj[self.header_list[4]] = w4[i].text
                self.header_obj[self.header_list[5]] = w5[i].text
                self.header_obj[self.header_list[6]] = w6[i].text
                self.header_obj[self.header_list[7]] = w7[i].text
                self.header_obj[self.header_list[8]] = w8[i].text
                self.header_obj[self.header_list[9]] = w9[i].text
                self.header_obj[self.header_list[10]] = w11[i].text
                self.write_csv(self.header_list, self.header_obj)
        except:
            self.driver.find_element_by_id("ctl00_ImageButton1").click()

    def write_csv(self, source_column, value):
        try:
            column = source_column.copy()
            column.extend(['station_code', 'station_name'])
            self.sl_no+=1
            print(self.sl_no)
            # value['sl_no'] = self.sl_no
            # value['station_code'] = self.station_code
            # value['station_name'] = self.station_name
            value['sl_no'], value['station_code'], value['station_name'] = self.sl_no, self.station_code, self.station_name
            with open(self.file_name, 'a', newline='', encoding='utf8') as csvfile:
                writer1 = csv.DictWriter(csvfile, fieldnames=column)
                if self.flag:
                    writer1.writeheader()
                    self.flag = False
                writer1.writerow(value)
        except:
            self.driver.find_element_by_id("ctl00_ImageButton1").click()
    # value for station
    def valueGetter(self, block_list):
        try:
            block_names = []
            for anchor in block_list:
                block_names.append(anchor.get_attribute('innerHTML'))
            return block_names
        except:
            self.driver.find_element_by_id("ctl00_ImageButton1").click()


if __name__ == "__main__":
    unittest.main()
