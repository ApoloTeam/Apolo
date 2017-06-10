# -*- coding:utf-8 -*-
from selenium import webdriver

def open():
    driver = webdriver.Firefox()
    url = 'http://www.baidu.com'
    driver.get(url)

if __name__ == "__main__":
    open()


# driver.close()
# import selenium
# print(selenium.__file__)

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

