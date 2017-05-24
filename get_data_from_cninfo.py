# # -*- coding: utf-8 -*-
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, os


# def start_chrome():
#     data_path = 'G:\\Program\Projects\Apolo\data'
#     options = webdriver.ChromeOptions()
#     prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': data_path}
#     options.add_experimental_option('prefs', prefs)
#     chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
#     os.environ["webdriver.chrome.driver"] = chrome_driver
#     cursor = webdriver.Chrome(executable_path=chrome_driver, chrome_options=options)
#     return cursor


class Get:
    def __init__(self, stock_id, sheet, from_year, to_year):
        # self.cursor = cursor
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

    # def download_sheet(self):
    #     cursor = self.start_chrome()
    #     cursor.implicitly_wait(30)  # 隐式等待
    #     cursor.get(self.base_url)
    #     cursor.find_element_by_link_text(u"个股财务数据").click()
    #     cursor.find_element_by_id("index_cw_input_obj").clear()
    #     cursor.find_element_by_id("index_cw_input_obj").send_keys(self.stock_id)
    #     cursor.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a').click()
    #
    #     sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
    #     sheet_type.select_by_value(self.sheet)
    #
    #     from_date = Select(cursor.find_element_by_id("cw_start_select_obj"))
    #     from_date.select_by_value(self.from_year)
    #     end_date = Select(cursor.find_element_by_id("cw_end_select_obj"))
    #     end_date.select_by_value(self.to_year)
    #     cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()

    def download_3_sheet3(self):
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
        self.download_3_sheet3()
        # self.input()


def control():
    fzb = Get('600100', 'fzb', '2015', '2016')
    fzb.action()
    # lrb = Get('600100', 'lrb', '2015', '2016')
    # lrb.operation()
#
#         # def is_element_present(self, how, what):
#         #     try:
#         #         self.driver.find_element(by=how, value=what)
#         #     except NoSuchElementException as e: return False
#         #     return True
#         #
#         # def is_alert_present(self):
#         #     try:
#         #         self.driver.switch_to.alert()
#         #     except NoAlertPresentException as e: return False
#         #     return True
#         #
#         # def close_alert_and_get_its_text(self):
#         #     try:
#         #         alert = self.driver.switch_to.alert()
#         #         alert_text = alert.text
#         #         if self.accept_next_alert:
#         #             alert.accept()
#         #         else:
#         #             alert.dismiss()
#         #         return alert_text
#         #
#         #     finally:
#         #         self.accept_next_alert = True
#         #
#         # def tearDown(self):
#         #     self.driver.quit()
#         #     self.assertEqual([], self.verificationErrors)
#
if __name__ == "__main__":
    # start_chrome()
    # cursor = start_chrome()
    # fzb = Get('600100', 'fzb', '2015', '2016')
    # fzb.operation()
    # # fzb.start_chrome()
    # lrb = Get('600100', 'lrb', '2015', '2016')
    # lrb.operation()
    control()
