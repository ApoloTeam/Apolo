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
# from collections import Iterable
from get_data_from_Tushare import *


class Get:
    def __init__(self, stock_id, sheet, from_year, to_year):
        self.base_url = "http://www.cninfo.com.cn/cninfo-new/index#"
        self.data_path = 'G:\\Program\Projects\Apolo\data'
        # self.data_path = './data'
        self.stock_id = stock_id
        self.stock_path = os.path.join(self.data_path, self.stock_id)
        self.sheet = sheet
        self.from_year = from_year
        self.to_year = to_year
        self.verificationErrors = []  # 脚本运行时，错误的信息将被打印到这个列表中
        self.accept_next_alert = True  # 是否继续接受下一下警告,字面意思,没找到解释

    def create_folder_stock_id(self):
        if os.path.exists(self.stock_path) is False:
            os.makedirs(self.stock_path)

    def start_chrome(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.stock_path}
        options.add_experimental_option('prefs', prefs)
        chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chrome_driver
        cursor = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
        cursor.implicitly_wait(30)  # 隐式等待
        return cursor

    def operation_script(self):
        cursor = self.start_chrome()
        cursor.get(self.base_url)
        cursor.find_element_by_link_text(u"个股财务数据").click()
        cursor.find_element_by_id("index_cw_input_obj").clear()
        cursor.find_element_by_id("index_cw_input_obj").send_keys(self.stock_id)
        cursor.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a').click()

        from_date = Select(cursor.find_element_by_id("cw_start_select_obj"))
        from_date.select_by_value(self.from_year)

        end_date = Select(cursor.find_element_by_id("cw_end_select_obj"))
        end_date.select_by_value(self.to_year)

        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("fzb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait(5)
        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("llb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait(5)
        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value("lrb")
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()
        # cursor.implicitly_wait(5)

    def action(self):
        self.create_folder_stock_id()
        self.operation_script()


def filter_stock_id(date):
    stock_list = pd.DataFrame(pd.read_csv('./data/stock_basics/20170601.csv', encoding='gbk'))
    stock_list = stock_list[(stock_list['timeToMarket'] < date)]
    stock_list = stock_list.sort_values(by=['code'], ascending=True)
    stock_list = stock_list['code'].tolist()
    return stock_list


def download(n):
    stock = Get(str(n).zfill(6), 'fzb', '2015', '2016')  # zfill is to fill up 0 to the left
    stock.action()


def control():
    stock_list = filter_stock_id(20120101)
    itr_stock_list = iter(stock_list)
    for stock_id in itr_stock_list:
        download(stock_id)

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
    control()
