# # -*- coding: utf-8 -*-
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, os


class Get:
    def __init__(self, stock_id, sheet, from_year, to_year):
        self.base_url = "http://www.cninfo.com.cn/cninfo-new/index#"
        self.data_path = 'G:\\Program\Projects\Apolo\data'
        self.stock_id = stock_id
        self.sheet_path = os.path.join(self.data_path, sheet)
        self.sheet = sheet
        self.from_year = from_year
        self.to_year = to_year
        self.verificationErrors = []  # 脚本运行时，错误的信息将被打印到这个列表中
        self.accept_next_alert = True  # 是否继续接受下一下警告,字面意思,没找到解释
        self.options = webdriver.ChromeOptions()
        self.prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.sheet_path}
        self.options.add_experimental_option('prefs', self.prefs)

    def input(self):
        chrome_driver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chrome_driver
        cursor = webdriver.Chrome(executable_path=chrome_driver, chrome_options=self.options)
        cursor.implicitly_wait(30)  # 隐式等待
        cursor.get(self.base_url)
        cursor.find_element_by_link_text(u"个股财务数据").click()
        cursor.find_element_by_id("index_cw_input_obj").clear()
        cursor.find_element_by_id("index_cw_input_obj").send_keys(self.stock_id)
        cursor.find_element_by_xpath('//*[@id="index_cw_stock_list"]/li[2]/a').click()

        sheet_type = Select(cursor.find_element_by_id("index_select_type_obj"))
        sheet_type.select_by_value(self.sheet)
        from_date = Select(cursor.find_element_by_id("cw_start_select_obj"))
        from_date.select_by_value(self.from_year)

        end_date = Select(cursor.find_element_by_id("cw_end_select_obj"))
        end_date.select_by_value(self.to_year)
        cursor.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()

    def operation(self):
        self.input()
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
    fzb = Get('600100', 'fzb', '2015', '2016')
    fzb.operation()
    lrb = Get('600100', 'lrb', '2015', '2016')
    lrb.operation()
