import re
import csv
import os.path
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

chrome_path = "K:/chromedriver_win32/chromedriver.exe"

class scrap:
    def __init__(self):
        self.sl_no = 0
        self.old_no = 0
        self.flag = True
        self.old_flag = True
        self.fieldnames = ['sl_no', 'date', 'District','Block', 'time' ,'temp', 'rh', 'wind_speed', 'pcip']
        d = date.today()
        date_day =  '-'.join(str(x) for x in (d.month, d.day, d.year))
        self.current_date = "current_" + date_day + ".csv"
        self.current_date = date_day
        self.previous_date = d - timedelta(1)
        print(self.previous_date)
        self.last_date = "weather_data.csv"
        self.driver = webdriver.Chrome(chrome_path)

    def createFile(self):
        if os.path.isfile(self.last_date):
            print('file already present')
        else:
            with open(self.last_date, 'a', newline='', encoding='utf8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                writer.writeheader()

    def writePreviousDateValue(self, districtName, block_name, value):
        self.old_no += 1
        with open(self.last_date, 'a', newline='', encoding='utf8') as csvfile:
            value['sl_no'] = self.old_no
            value['date'] =  self.previous_date
            value['District'] = districtName
            value['Block'] = block_name
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            # if self.old_flag:
            #     writer.writeheader()
            #     self.old_flag = False
            writer.writerow(value)

    def writeCurrentDateValue(self, districtName, block_name, value):
        self.sl_no += 1
        with open(self.current_date, 'a', newline='', encoding='utf8') as csvfile:
            value['sl_no'] = self.sl_no
            value['District'] = districtName
            value['Block'] = block_name
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            if self.flag:
                writer.writeheader()
                self.flag = False
            writer.writerow(value)

    def CurrentDataWrite(self, districtName, block_name):
        value = {}
        dataValue = self.driver.find_elements_by_xpath('// *[ @ id = "DynamicWeatherDataDiv"] / div')
        count = dataValue.__len__()
        if count <= 1:
            value['temp'] = 'No data'
            value['rh'] = 'No data'
            value['wind_speed'] = 'No data'
            value['pcip'] = 'No data'
            value['time'] = 'No data'
            self.writeCurrentDateValue(districtName, block_name, value)
        else:
            time = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w1"]'),'none')
            temp = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w2"]'), 'none')
            rh = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w3"]'), 'none')
            wind_speed = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w4"]'), 'none')
            for idx, item in enumerate(dataValue):
                value['temp'] = temp[idx]
                value['rh'] = rh[idx]
                value['wind_speed'] = wind_speed[idx]
                value['pcip'] = 'No data'
                value['time'] = time[idx]
                self.writeCurrentDateValue(districtName, block_name, value)
        # self.driver.back()

    def previousDataWrite(self, districtName, block_name):
        value = {}
        dataValue = self.driver.find_elements_by_xpath('// *[ @ id = "DynamicWeatherDataDiv"] / div')
        count = dataValue.__len__()
        if count <= 1:
            value['temp'] = 'No data'
            value['rh'] = 'No data'
            value['wind_speed'] = 'No data'
            value['pcip'] = 'No data'
            value['time'] = 'No data'
            self.writePreviousDateValue(districtName, block_name, value)
        else:
            time = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w1"]'),'none')
            temp = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w2"]'), 'none')
            rh = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w3"]'), 'none')
            wind_speed = self.valueGetter(self.driver.find_elements_by_xpath('//*[@class="w4"]'), 'none')
            for idx, item in enumerate(dataValue):
                value['temp'] = temp[idx]
                value['rh'] = rh[idx]
                value['wind_speed'] = wind_speed[idx]
                value['pcip'] = 'No data'
                value['time'] = time[idx]
                self.writePreviousDateValue(districtName, block_name, value)

        self.driver.back()
        self.driver.back()

    def valueGetter(self, block_list, type):
        block_names = []
        if(type == "district"):
            block_names.append("All")

        for anchor in block_list:
            block_names.append(anchor.get_attribute('innerHTML'))
        return block_names

    def BlockClick(self,districtName):
        select_anchor = self.driver.find_elements_by_xpath("//div[@class='w1']/a")
        block_name = self.valueGetter(select_anchor, "block")
        print(block_name)
        select = Select(self.driver.find_element_by_id("ddlBlock"))
        option = select.options
        for number in range(1, option.__len__()):
            try:
                select = Select(self.driver.find_element_by_id("ddlBlock"))
                select.select_by_index(number)
                self.CurrentDataWrite(districtName, block_name[number - 1])
            except:
                print('district - ' + districtName + ' block - '+ block_name[number - 1])
                #self.CurrentDataWrite(districtName, block_name[number - 1])
                previous = self.driver.find_element_by_link_text("Last Day")
                previous.click()
                self.previousDataWrite(districtName, block_name[number - 1])
        self.driver.back()

    def DistrictClick(self, anchor_list):
        select = Select(self.driver.find_element_by_id("ddlDistrict"))
        option = select.options
        district_name = self.valueGetter(option , "null")
        print(district_name)
        for number in range(1, district_name.__len__()):
            try:
                select = Select(self.driver.find_element_by_id("ddlDistrict"))
                select.select_by_index(number)
                self.BlockClick(district_name[number])
            except:
                self.BlockClick(district_name[number])
                print("This is an error message!")
        self.driver.back()

    def selenium(self):
        self.createFile()
        driver = self.driver
        QueryFormatString = 'http://tawn.tnau.ac.in/'
        driver.get(QueryFormatString)
        button = driver.find_element_by_xpath('// *[ @ id = "menu"] / ul / li[2] / a')
        button.click()
        cur_win = driver.current_window_handle
        select_anchor = driver.find_elements_by_xpath("//div[@class='w1']/a")
        select = Select(self.driver.find_element_by_id("ddlDistrict"))
        options = select.options
        self.DistrictClick(select_anchor)
        self.driver.close()


scrapping = scrap()
scrapping.selenium()



