# # -*- coding: utf-8 -*-
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, os
import pandas as pd
import zipfile as zip
from get_data_from_Tushare import *


class GetFromCninfo:
    def __init__(self):
        self.base_url = "http://www.cninfo.com.cn/cninfo-new/index#"
        self.data_path = 'G:\\Program\Projects\Apolo\data'
        # self.data_path = './data'
        self.verificationErrors = []  # 脚本运行时，错误的信息将被打印到这个列表中
        self.accept_next_alert = True  # 是否继续接受下一下警告,字面意思,没找到解释

    def create_folder_stock_id(self, stock_id):
        stock_path = os.path.join(self.data_path, stock_id)
        if os.path.exists(stock_path) is False:
            os.makedirs(stock_path)

    def start_chrome(self, stock_id):
        options = webdriver.ChromeOptions()
        stock_path = os.path.join(self.data_path, stock_id)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': stock_path}
        options.add_experimental_option('prefs', prefs)
        chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chrome_driver
        cursor = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
        cursor.implicitly_wait(30)  # 隐式等待
        return cursor

    def operation_script(self, stock_id, from_year, to_year):
        cursor = self.start_chrome(stock_id)
        cursor.get(self.base_url)
        cursor.find_element_by_link_text(u"个股财务数据").click()
        cursor.find_element_by_id("index_cw_input_obj").clear()
        cursor.find_element_by_id("index_cw_input_obj").send_keys(stock_id)
        cursor.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a').click()

        from_date = Select(cursor.find_element_by_id("cw_start_select_obj"))
        from_date.select_by_value(from_year)

        end_date = Select(cursor.find_element_by_id("cw_end_select_obj"))
        end_date.select_by_value(to_year)

        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("fzb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait
        time.sleep(1)
        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("llb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait(5)
        time.sleep(1)
        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("lrb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait(5)
        time.sleep(1)
        cursor.close()

    def download(self, stock_id, from_year, to_year):
        self.create_folder_stock_id(stock_id)
        self.operation_script(stock_id, from_year, to_year)

    def unzip(self, stock_id):
        stock_path = os.path.join(self.data_path, stock_id)
        file_list = os.listdir(stock_path)
        for file_name in file_list:
            if os.path.splitext(file_name)[1] == '.zip':
                # print(file_name)
                file_zip = zip.ZipFile(os.path.join(stock_path, file_name), 'r')
                # print(file_zip.read(file_zip.namelist()[0]))
                for file in file_zip.namelist():
                    file_zip.extract(file, stock_path)
                file_zip.close()


class DownloadOneStock(GetFromCninfo):
    def download_unzip(self, stock_id, from_year, to_year):
        self.download(stock_id, from_year, to_year)
        time.sleep(2)
        self.unzip(stock_id)


class DownloadStocks(GetFromCninfo):
    @staticmethod
    def filter_stock_list(date):
        stock_list = pd.DataFrame(pd.read_csv('./data/stock_basics/20170601.csv', encoding='gbk'))
        stock_list = stock_list[(stock_list['timeToMarket'] < date)]
        stock_list = stock_list.sort_values(by=['code'], ascending=True)
        stock_list = stock_list['code'].tolist()
        return stock_list

    def download_stock_list(self, from_year, to_year, date):
        stock_list = self.filter_stock_list(date)
        itr_stock_list = iter(stock_list)
        for stock_id in itr_stock_list:
            self.download(str(stock_id).zfill(6), from_year, to_year)
            time.sleep(1)
            self.unzip(str(stock_id).zfill(6))

        # def is_element_present(self, how, what):
        #     try:
        #         self.driver.find_element(by=how, value=what)
        #     except NoSuchElementException as e: return False
        #     return True
        #
        # def is_alert_present(self):
        #     try:
        #         self.driver.switch_to.alert()
        #     except NoAlertPresentException as e: return False
        #     return True
        #
        # def close_alert_and_get_its_text(self):
        #     try:
        #         alert = self.driver.switch_to.alert()
        #         alert_text = alert.text
        #         if self.accept_next_alert:
        #             alert.accept()
        #         else:
        #             alert.dismiss()
        #         return alert_text
        #
        #     finally:
        #         self.accept_next_alert = True
        #
        # def tearDown(self):
        #     self.driver.quit()
        #     self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    # control()
    # one_stock = DownloadOneStock()
    # one_stock.download_unzip('000001', '2015', '2016')
    multi_stocks = DownloadStocks()
    multi_stocks.download_stock_list('2015', '2016', 20120101)
