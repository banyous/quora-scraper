# -*- coding: utf-8 -*-
import os
import pathlib
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
DEBUG = 1
def connectchrome():
    options = Options()
    # if you want to hide browser window, uncomment line below
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-dev-shm-usage");
    driver_path= Path.cwd() / "chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.maximize_window()
    time.sleep(2)
    return driver
