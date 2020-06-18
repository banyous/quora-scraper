# -*- coding: utf-8 -*-
import sys
import pathlib
from pathlib import Path
sys.path
DEBUG = 1
import os
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import dateparser
from connectChrome import connectchrome

# -------------------------------------------------------------
# -------------------------------------------------------------
def convertnumber(number):
    if 'k' in number:
        n=float(number.replace('k', '').replace(' ', ''))*1000
    elif 'm' in number:
        n=float(number.replace('m', '').replace(' ', ''))*1000000
    else:
        n=number
    return int(n)   

# -------------------------------------------------------------
# -------------------------------------------------------------
# method for loading all Quora answers ( a default Quora Question page shows only 7 Answers)
def scrolldown(self):
    last_height = self.page_source
    loop_scroll=True
    attempt = 0
    # we generate a random waiting time between 2 and 4
    waiting_scroll_time=round(random.uniform(2, 4),1)
    print('scrolling down to get all answers...')
    while loop_scroll:
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.execute_script("window.scrollBy(0,-200)")
        time.sleep(1)
        self.execute_script("window.scrollBy(0,-200)")
        time.sleep(1)
        new_height=self.page_source
        if new_height == last_height:
            # in case of not change, we increase the waiting time
            waiting_scroll_time= round(random.uniform(5, 7),1)
            attempt += 1
            if attempt==3:# in the third attempt we end the scrolling
                loop_scroll=False
            #print('attempt',attempt)
        else:
            attempt=0
            waiting_scroll_time=round(random.uniform(2, 4),1)
        last_height=new_height
    posts = self.find_elements_by_css_selector("div.AnswerBase")
    #print(" total answers found : ",len(posts))


# -------------------------------------------------------------
# -------------------------------------------------------------
# main crawling function
def answers(param, urls_file_or_list, list_index):
    urls_list = []
    if param.strip().lower() == '-f':
        # read Questions URLs
        try:
            if Path(urls_file_or_list).is_file():
                URLs_file = open(urls_file_or_list, mode='r', encoding='utf-8')
            else:# if file not found, we try to open it in the local dir
                URLs_file =  open(Path.cwd() / urls_file_or_list, mode='r', encoding='utf-8')
            urls_file = open(urls_file_or_list, mode='r', encoding='utf-8')
            urls_list = urls_file.readlines()
            urls_file.close()
            urls_list = [t.strip() for t in urls_list]
        except:
            print('Error: invalid file path. Please make sure to provide the correct path to the topic file')
            print('Or put the topic file in the quora_scraper/ directory :',Path.cwd())
            sys.exit(1)
    elif str(param).strip().lower() == '-k':
        try:
            urls_list = [e for e in urls_file_or_list.strip('[]').split(',')]
        except:
            print(
                "Error: invalid topics keyword list format. Please provide valid list format such as: ['key1','key2','key3'] ")
    else:
        print('Error: invalid parameter value. Please only choose between -k and -f parameters')

    # Open question urls file (save file)
    pathlib.Path('Answers').mkdir(parents=True, exist_ok=True)
    save_file_path= Path.cwd() / Path("Answers")/ "answers.txt"
    file_answers = open(save_file_path, mode='a') # output file containing all answers
    browser= connectchrome()
    # starting line
    k = int(list_index)
    limit= len(urls_list)
    #print('limit ',limit)
    print('Starting the questions crawling')
    while True:
        print('--------------------------------------------------')
        if k >= limit:
            print('crawling in completed')
            break
        current_line = urls_list[k]
        print('processing question number  : '+ str(k+1))
        print(current_line)
        k += 1
        if '/unanswered/' in str(current_line):
            print('answer is unanswered')
            continue
        question_id = current_line
        # opening Question page
        try:
            browser.get(current_line)
        except Exception as OpenEx:
            print('cant open the following question link : ',current_line)
            #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(OpenEx).__name__, OpenEx)
            #print(str(OpenEx))
            continue
        try:
            nb_answers_text = WebDriverWait(browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='QuestionPageAnswerHeader']//div[@class='answer_count']"))).text
        except:
            print('cant get answers')
            continue
        #nb_answers_text = browser.find_element_by_xpath("//div[@class='QuestionPageAnswerHeader']//div[@class='answer_count']").text
        nb_answers=[int(s.strip('+')) for s in nb_answers_text.split() if s.strip('+').isdigit()][0]
        print('Question have :', nb_answers_text)
        if nb_answers>7:
            scrolldown(browser)
        continue_reading_buttons = browser.find_elements_by_xpath("//a[@role='button']")
        time.sleep(2)
        for button in continue_reading_buttons:
            try:
                ActionChains(browser).click(button).perform()
                time.sleep(1)
            except:
                continue
        time.sleep(2)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source,"html.parser")
        # get the question-id
        question_id = current_line.rsplit('/', 1)[-1]
        # find title 
        title= current_line.replace("https://www.quora.com/","")
        # find question's topics
        questions_topics= soup.findAll("span", {"class": "TopicName"})
        questions_topics_text=[]
        for topic in questions_topics : questions_topics_text.append(topic.text)
        # number of answers
        # not all answers are saved!
        # answers that collapsed, and those written by annonymous users are not saved
        try:
            split_html = html_source.split('class="pagedlist_item"')
        except Exception as notexist :#mostly because question is deleted by quora
            print('question no long exists')
            #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(notexist).__name__, notexist)
            #print(str(notexist))
            continue    
        # The underneath loop will generate len(split_html)/2 exceptions, cause answers in split_html
        # are eitheir in Odd or Pair positions, so ignore printed exceptions.
        for i in range(1, len(split_html)):
            try:
                part = split_html[i]
                part_soup = BeautifulSoup(part,"html.parser" )
                #print('===============================================================')
                #find users names of answers authors
                authors=  part_soup.find("a", {"class": "u-flex-inline"}, href=True)
                user_id = authors['href'].rsplit('/', 1)[-1]
                #print(user_id)
                # find answer dates
                answer_date= part_soup.find("a", {"class": "answer_permalink"})
                try:
                    date=answer_date.text
                    if ("Updated" in date):
                       date= date[8:]
                    else:
                       date= date[9:]
                    date=dateparser.parse(date).strftime("%Y-%m-%d")
                except: # when updated or answered in the same week (ex: Updated Sat)
                    date=dateparser.parse("7 days ago").strftime("%Y-%m-%d")
                #print(date)
                # find answers text
                answer_text = part_soup.find("div", {"class": "ui_qtext_expanded"})
                # print(" answer_text", answer_text)
                answer_text = answer_text.text
                #write answer elements to file
                s=  str(question_id) +'\t' + str(date) + "\t"+ user_id + "\t"+ str(questions_topics_text) + "\t" +    str(answer_text)  + "\n"
                #print("wrting down the answer...")
                file_answers.write(s)
            except Exception as e1: # Most times because user is anonymous ,  continue without saving anything
               # print('---------------There is an Exception-----------')
                #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e1).__name__, e1)
                #print(str(e1))
                o=1

        # we sleep every while in order to avoid IP ban
        if k%5==4:
            sleep_time=(round(random.uniform(5, 10),1))
            # print('*********')
            # print('Seleeping the browser for ', sleep_time)
            # print('*********')
            time.sleep(sleep_time)

    print('answers saved to : ',save_file_path)
    browser.quit()
