#!/usr/bin/env python
DEBUG = 1
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def connectchrome():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('log-level=3')
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        import quora_scraper
        package_path=str(quora_scraper.__path__).split("'")[1]
        driver_path= Path(package_path) / "chromedriver"
    except:
        driver_path= Path.cwd() / "chromedriver"
    driver_path= Path(package_path) / "chromedriver"
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    browser.maximize_window()
    browser.set_window_position(70, 0, windowHandle ='current')
    time.sleep(2)
    return browser

def scrolldown(self):
    print('scrolling down to get all answers...')
    last_height = self.page_source
    loop_scroll=True
    attempt = 0
    # scroll down loop until page not changing
    while loop_scroll:
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height=self.page_source
        if new_height == last_height:
            # in case of not change, we increase the waiting time
            attempt += 1
            if attempt==3:# in the third attempt we end the scrolling
                loop_scroll=False
        else:
            attempt=0
        last_height=new_height

def scrollup_alittle(self,nbtimes):
    for iii in range(0,nbtimes):
        self.execute_script("window.scrollBy(0,-400)")
        time.sleep(1)

def click_on_all(browser, find_by, selector):
    last_nb_buttons = -1
    last_nb_buttons_repeated = 0
    while True:
        buttons = find_by(selector)
        nb_buttons = len(buttons)

        print('clicking on ', nb_buttons, 'instances of ', '"' + selector + '"')
        for button in buttons:
            ActionChains(browser).move_to_element(button).click(button).perform()
            time.sleep(0.5)

        # know when to exit the loop
        if nb_buttons == 0:
            break
        elif nb_buttons == last_nb_buttons:
            last_nb_buttons_repeated += 1
            # if we keep seeing the same number of buttons, the buttons are probably broken
            if last_nb_buttons_repeated == 10:
                break
        else:
            last_nb_buttons = nb_buttons
            last_nb_buttons_repeated = 0


def show_more_of_articles(browser):
    click_on_all(browser, browser.find_elements_by_xpath, "//div[contains(text(), '(more)')]")

def view_more_comments(browser):
    click_on_all(browser, browser.find_elements_by_xpath, "//div[text()[contains(., 'View More Comments')]]")

def view_collapsed_comments(browser):
    click_on_all(browser, browser.find_elements_by_xpath, "//div[text()[contains(., 'View Collapsed Comments')]]")

def expand_hidden_comments(browser):
    click_on_all(browser, browser.find_elements_by_css_selector, ".qu-tapHighlight--white .qu-pb--tiny")

def view_more_replies(browser):
    click_on_all(browser, browser.find_elements_by_xpath, "//div[text()[contains(., 'View More Replies')]]")

def show_more_of_comments(browser):
    click_on_all(browser, browser.find_elements_by_xpath, "//span[contains(text(), '(more)')]")
