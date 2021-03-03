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
    try_again, \
    connectchrome

###############################################################
parser=argparse.ArgumentParser()
parser.add_argument("user", help="The user ID you want to visit")
args=parser.parse_args()

user = args.user
url = "https://www.quora.com/profile/" + user
print("opening", url)
browser = connectchrome()
browser.get(url)
time.sleep(2)

nbanswers = browser.find_element_by_xpath("//div[text()[contains(.,'Answers')]]")
nbanswers = nbanswers.text.strip('Answers').strip().replace(',', '')
print('user has ', nbanswers, ' answers')
###############################################################

def do_scrolldown():
    print(do_scrolldown.__name__ + "()")
    scrolldown(browser)

def do_show_more_of_articles():
    print(do_show_more_of_articles.__name__ + "()")
    show_more_of_articles(browser)

def do_view_more_comments():
    print(do_view_more_comments.__name__ + "()")
    view_more_comments(browser)

def do_view_collapsed_comments():
    print(do_view_collapsed_comments.__name__ + "()")
    view_collapsed_comments(browser)

def do_expand_hidden_comments():
    print(do_expand_hidden_comments.__name__ + "()")
    expand_hidden_comments(browser)

def do_view_more_replies():
    print(do_view_more_replies.__name__ + "()")
    view_more_replies(browser)

def do_show_more_of_comments():
    print(do_show_more_of_comments.__name__ + "()")
    show_more_of_comments(browser)

def do_try_again():
    print(do_try_again.__name__ + "()")
    try_again(browser)

def do_all():
    print(do_all.__name__ + "()")
    do_scrolldown()
    do_show_more_of_articles()
    do_view_more_comments()
    do_view_collapsed_comments()
    do_expand_hidden_comments()
    do_view_more_replies()
    do_show_more_of_comments()
    do_try_again()

###############################################################

do_all()
do_all()
do_all()
do_all()
do_all()
do_all()

print("now you can manually check if there is any work left to be done by typing 'do_' and then Tab to show you the "
      "commands you can use to manually keep expanding the articles and comments. Choose the command you want to "
      "call, close the parenthesis and hit Enter. E.g. you could type 'do_all()' and Enter to run all the commands "
      "in sequence again.")

# also check the page for "Try Again" from Connection errors !
# and remove position: fixed for search bar before printint
