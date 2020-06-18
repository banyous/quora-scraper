from .connectChrome import connectchrome
from bs4 import BeautifulSoup
import os
import pathlib
from pathlib import Path
import datetime
import time
import csv
import sys
import ast

# -------------------------------------------------------------
# -------------------------------------------------------------
def convertnumber(number):
    if 'k' in number:
        n=float(number.lower().replace('k', '').replace(' ', ''))*1000
    elif 'm' in number:
        n=float(number.lower().replace('m', '').replace(' ', ''))*1000000
    else:
        n=number
    return int(n)

# -------------------------------------------------------------
# -------------------------------------------------------------
#main crawling function

def questions(param, topics_file_or_list, line_index=0):
    topics_list = []
    if param.strip().lower()=='-f':
        try:
            # read topics
            if Path(topics_file_or_list).is_file():
                topics_file = open(topics_file_or_list, mode='r', encoding='utf-8')
            else:  # if file not found, we try to open it in the local dir
                topics_file = open(Path.cwd() / topics_file_or_list, mode='r', encoding='utf-8')
            topics_list = topics_file.readlines()
            topics_file.close()
            topics_list=[t.strip() for t in topics_list]
        except:
            print('Error: invalid file path. Please make sure to provide the correct to the topic file')
    elif str(param).strip().lower() =='-k':
        try:
            topics_list =  [e for e in topics_file_or_list.strip('[]').split(',')]
        except:
            print("Error: invalid topics keyword list format. Please provide valid list format such as: ['key1','key2','key3'] ")
    else:
        print('Error: invalid parameter value. Please only choose between -k and -f parameters')

    # the topic parsing index  ,
    # If program stops for any reason After running
    # you can manually change the topic_index to last parsed topic's index
    topic_index=int(line_index)
    #connecting to chrome ..
    browser=connectchrome()
    # loop over topics_list
    loop_limit=len(topics_list)
    while True:
        if topic_index>=loop_limit:
            print('---------------------------------')
            print('Crawling completed...')
            print('Question URLs saved to : ', save_path)
            break
        topic_term = topics_list[topic_index].strip()
        topic_index += 1
        # we remove hashtags (optional)
        topic_term.replace("#",'')

        # Looking if the topic has an existing Quora url
        print('#########################################################')
        print('Looking for topic number : ',topic_index,' | ', topic_term)
        try:
            url = "https://www.quora.com/topic/" + topic_term.strip() + "/all_questions"
            browser.get(url)
        except Exception as e0:
            print('topic does not exist in Quora')
            # print('exception e0')
            # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e0).__name__, e0)
            continue

        # get browser source
        html_source = browser.page_source
        question_count_soup = BeautifulSoup(html_source, 'html.parser')

        #  get total number of questions
        question_count_str = question_count_soup.find('a', attrs={'class': 'TopicQuestionsStatsRow'})
        if str(question_count_str) =='None':
            print('topic does not have questions...')
            continue
        question_count = convertnumber(question_count_str.contents[0].text)
        question_count_str = question_count_soup.find('a', attrs={'class': 'TopicQuestionsStatsRow'})
        if question_count ==0:
            print('topic does not have questions...')
            continue
        print('number of questions for this topic : '+ str(question_count))

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")

        # infinite while loop, break it when you reach the end of the page or not able to scroll further.
        # Note that Quora
        if int(question_count)>10: # if there is more than 10 questions, we need to scroll down the profile to load remaining questions
            start_time_sd = time.time()
            max_time=  int(question_count)*0.25
            if int(question_count)> 8000:
                max_time=1800
            while True:
                scrolling_attempt = 0
                scroll_waiting_time = 2
                # try to scroll 3 times in case of slow connection
                while True:
                    #print('@@@@@@@@@@@@@@@@@@@@!trying for time number ',scrolling_attempt)
                    # Scroll down to one page length
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(scroll_waiting_time)
                    # get page height in pixels
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    # break this loop when you are able to scroll further
                    if new_height != last_height:
                       break
                    # else  we do 3 attempts of scrolling down with different pause_time in each attempt
                    scrolling_attempt+=1
                    if scrolling_attempt==1:
                        scroll_waiting_time = 4
                    elif scrolling_attempt==2:
                        if int(question_count)>2000:
                            scroll_waiting_time = 15
                        elif int(question_count)>500:
                            scroll_waiting_time = 7
                        else : # if number of questions is small(<500) than quit
                            break
                    else : # after the third attempt we quit
                        break
                if new_height == last_height:  # not able to scroll further, break the loop
                    break
                last_height = new_height
                # check if the  total time exceeds the limit
                total_time=time.time() - start_time_sd
                if total_time> max_time:
                    #print('max time exceeded')
                    break

        # next we harvest all questions URLs that exists in the Quora topic's page
        # get html page source
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # question_link is the class for questions
        question_link = soup.find_all('a', attrs={'class': 'question_link'}, href=True)

        # add questions to a set for uniqueness
        question_set = set()
        for ques in question_link:
            question_set.add(ques)

        # write content of set to Qyestions_URLs/ folder
        questions_directory = 'Questions_URLs/'
        pathlib.Path('Questions_URLs').mkdir(parents=True, exist_ok=True)
        save_path = Path.cwd() / Path("Questions_URLs")
        save_file= save_path /  str(topic_term.strip('\n') + '_question_urls.txt')
        file_question_urls = open(save_file, mode='w', encoding='utf-8')
        writer = csv.writer(file_question_urls)
        for ques in question_set:
            link_url = "http://www.quora.com" + ques.attrs['href']
            #print(link_url)
            writer.writerows([[link_url]])
        # sleep every while in order to not get banned
        if topic_index % 5 == 4:
            sleep_time = (round(random.uniform(5, 10), 1))
            # print('*********')
            # print('Seleeping the browser for ', sleep_time)
            # print('*********')
            time.sleep(sleep_time)

    browser.quit()
