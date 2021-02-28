#!/usr/bin/env python
DEBUG = 1
import time

from shared import \
    scrolldown, \
    show_more_of_articles, \
    view_more_comments, \
    view_more_replies, \
    view_collapsed_comments, \
    expand_hidden_comments, \
    show_more_of_comments, \
    connectchrome

###############################################################
browser = connectchrome()
browser.get("https://www.quora.com/profile/Artem-Boytsov")
time.sleep(2)

nbanswers = browser.find_element_by_xpath("//div[text()[contains(.,'Answers')]]")
nbanswers = nbanswers.text.strip('Answers').strip().replace(',', '')
print('user has ', nbanswers, ' answers')


###############################################################

def do_scrolldown():
    scrolldown(browser)


def do_show_more_of_articles():
    show_more_of_articles(browser)


def do_view_more_comments():
    view_more_comments(browser)


def do_view_more_replies():
    view_more_replies(browser)


def do_view_collapsed_comments():
    view_collapsed_comments(browser)


def do_expand_hidden_comments():
    expand_hidden_comments(browser)


def do_show_more_of_comments():
    show_more_of_comments(browser)
