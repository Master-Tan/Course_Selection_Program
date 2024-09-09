'''
author:Tan
'''

import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import random

class RefreshCookie():

    def __init__(self):
        pass

    @classmethod
    def run(self) -> None:
        username = 'zy2406229'  # 学生账号
        password = 'zwt20021001.'  # 密码
        path = "chromedriver/chromedriver-128.0.6613.114.exe"

        service = Service(executable_path=path)
        opt = webdriver.ChromeOptions()
        opt.add_argument('headless')
        opt.add_experimental_option("excludeSwitches",
                                    ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(service=service, options=opt)
        driver.get(r'https://yjsxk.buaa.edu.cn/yjsxkapp/sys/xsxkappbuaa/index.html')
        time.sleep(2)

        # 寻找所有button
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        # 点击登录按钮
        for button in buttons:
            if button.text == '点击进入登录':
                button.click()
                break
        time.sleep(2)

        frame = driver.find_element('id', 'loginIframe')
        driver.switch_to.frame(frame)
        driver.find_element(By.ID, 'unPassword').send_keys(username)
        driver.find_element(By.ID, 'pwPassword').send_keys(password)
        driver.find_element(By.CLASS_NAME, 'default-bgcolor').click()
        time.sleep(2)

        # 进入article
        driver.switch_to.default_content()

        # 获得header中的cookie
        cookies = driver.get_cookies()
        cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

        with open('cookie.txt', 'w', encoding='utf-8') as f:
            f.write(str(cookie_header))

        print('Cookie refreshed')