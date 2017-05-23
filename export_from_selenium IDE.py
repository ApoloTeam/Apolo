# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class get():
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://change-this-to-the-site-you-are-testing/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_222(self):
        driver = self.driver
        driver.get("http://www.cninfo.com.cn/cninfo-new/index")
        driver.find_element_by_link_text(u"个股财务数据").click()
        driver.find_element_by_id("hqkaptchaImage").click()
        driver.find_element_by_id("cwkaptchaImage").click()
        driver.find_element_by_id("index_cw_input_obj").clear()
        driver.find_element_by_id("index_cw_input_obj").send_keys("60")
        driver.find_element_by_link_text(u"000601A股韶能股份").click()
        Select(driver.find_element_by_id("cw_end_select_obj")).select_by_visible_text("2016")
        driver.find_element_by_css_selector("#con-f-2 > div.index-search > div.down_button_row > button.index_down_button").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    test = get()
