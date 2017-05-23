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
