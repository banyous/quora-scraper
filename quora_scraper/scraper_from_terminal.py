#!/usr/bin/env python
import argparse

DEBUG = 1
import time

from shared import \
    scrolldown, \
    show_more_of_articles, \
    view_more_comments, \
    view_collapsed_comments, \
    expand_hidden_comments, \
    view_more_replies, \
    show_more_of_comments, \
    connectchrome

###############################################################
parser=argparse.ArgumentParser()
parser.add_argument("user", help="The user ID you want to visit")
args=parser.parse_args()

user = args.user
url = "https://www.quora.com/profile/" + user
print("getting", url)
browser = connectchrome()
browser.get(url)
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

def do_view_collapsed_comments():
    view_collapsed_comments(browser)

def do_expand_hidden_comments():
    expand_hidden_comments(browser)

def do_view_more_replies():
    view_more_replies(browser)

def do_show_more_of_comments():
    show_more_of_comments(browser)

###############################################################

do_scrolldown()
do_show_more_of_articles()
do_view_more_comments()
do_view_collapsed_comments()
do_expand_hidden_comments()
do_view_more_replies()
do_show_more_of_comments()

# also check the page for "Try Again" from Connection errors !
# and remove position: fixed for search bar before printint
