# -*- coding: utf-8 -*-
DEBUG = 1
import os
import pathlib
from pathlib import Path
import time
import subprocess
import json
import sys
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from connectChrome import connectchrome
from datetime import datetime, timedelta
import dateparser

# -------------------------------------------------------------
# -------------------------------------------------------------
# remove 'k'(kilo) and 'm'(million) from Quora numbers
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
# convert Quora dates (such as 2 months ago) to DD-MM-YYYY format
def convertDateFormat(dateText):
    try:
        if ("Updated" in dateText):
            date = dateText[8:]
        else:
            date = dateText[9:]
        date = dateparser.parse(dateText).strftime("%Y-%m-%d")
    except:  # when updated or answered in the same week (ex: Updated Sat)
        date = dateparser.parse("7 days ago").strftime("%Y-%m-%d")
    return date

# -------------------------------------------------------------
# -------------------------------------------------------------
# for loading all profile content
def scrolldown(browser, repeat):
    print("scrolling down profile in order to load all User's answers...")
    src_updated = browser.page_source
    src = ""
    scroll_attempt=0
    sleep=2
    scrollcount=0
    while  True:
        scrollcount+=1
        if scrollcount>30: # we will scroll down max 30 times, in order to get only last 300 answers
            break
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep)
        src = src_updated
        src_updated = browser.page_source
        if src == src_updated:
            if repeat==True:
                scroll_attempt+=1
                if scroll_attempt==1:
                    sleep=10
                else:
                    break
            else:
                break

        else:
            scroll_attempt=0
            sleep=2

# -------------------------------------------------------------
# -------------------------------------------------------------
# Main crawling function
def users(param, users_file_or_list, list_index):
    users_list = []
    if param.strip().lower() == '-f':
        try:
            # read topics
            if Path(users_file_or_list).is_file():
                users_file = open(users_file_or_list, mode='r', encoding='utf-8')
            else:
                users_file =  open(Path.cwd() / users_file_or_list, mode='r', encoding='utf-8')
            users_list = users_file.readlines()
            users_file.close()
            users_list = [t.strip() for t in users_list]
        except Exception as ee:
            print('Error: invalid file path. Please make sure to provide the correct to the topic file')
            print(ee)
    elif str(param).strip().lower() == '-k':
        try:
            users_list =[e for e in users_file_or_list.strip('[]').split(',')]
        except:
            print(
                "Error: invalid topics keyword list format. Please provide valid list format such as: ['key1','key2','key3'] ")
    else:
        print('Error: invalid parameter value. Please only choose between -k and -f parameters')


    ##### two lines below are proxy parameters (use them if you have many proxies)
    # os.environ['http_proxy']=proxies[proxy_index]
    # current_proxy_index=proxy_index

    browser= connectchrome()
    wait = WebDriverWait(browser, 10)
    # find starting line : current line, which starts from the index of last crawled user
    current_index = int(list_index)-1

    # Loop over the QuoraIDs to scrap their profile content
    while True:
        print('_______________________________________________________________')
        current_index+=1
        if current_index >=len(users_list):
            print('Crawling finished...user profiles saved to : ',save_path)
            break
        # a dict to contain information about profile 
        quora_profile_information=dict()
        current_line= users_list[current_index].strip()
        current_line=current_line.replace('http', 'https')
        # we change proxy and sleep every 200 request (number can be changed)
        # sleep every while in order to not get banned
        if current_index % 5 == 4:
            sleep_time = (round(random.uniform(5, 10), 1))
            # print('*********')
            # print('Seleeping the browser for ', sleep_time)
            # print('*********')
            time.sleep(sleep_time)
        user_id=current_line.strip().replace('\r', '').replace('\n', '')
        url= "https://www.quora.com/profile/"+user_id
        print('processing quora user number : ', current_index +1, '    ', url)
        browser.get(url)        
        time.sleep(2) 
        # get profile description
        try: 
            description= browser.find_element_by_class_name('IdentityCredential')
            description= description.text.replace('\n', ' ')
            #print(description)
        except:
            description=''
            #print('no description')
        quora_profile_information['description']=description
        # get profile bio        
        try:
           more_button = browser.find_elements_by_link_text('(more)')
           ActionChains(browser).move_to_element(more_button[0]).click(more_button[0]).perform()
           time.sleep(0.5)
           profile_bio = browser.find_element_by_class_name('ProfileDescriptionPreviewSection')
           profile_bio_text=profile_bio.text.replace('\n', ' ')
           #print(profile_bio_text)
        except Exception as e:
           #print('no profile bio')
           #print(e)
           profile_bio_text=''
        quora_profile_information['profile_bio']=profile_bio_text
        html_source = browser.page_source
        source_soup = BeautifulSoup(html_source,"html.parser")
        #get location 
        #print('trying to get location')
        location='None'
        try:
            location1= (source_soup.find(attrs={"class":"LocationCredentialListItem"}))
            location2= (location1.find(attrs={"class":"main_text"})).text
            location= location2.replace('Lives in ','')
        except Exception as e3:
            #print('exception regarding finding location')
            #print(e3)
            pass
        quora_profile_information['location']=location
        #get total number of views
        total_views='0'
        try:
            #views=wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "AnswerViewsAboutListItem.AboutListItem")))
            views= (source_soup.find(attrs={"class":"ContentViewsAboutListItem"}))            
            total_views=views.text.split("content")[0]
        except Exception as e4:
            ###print('exception regarding finding number of views')
            ###print(e4)
            pass
        #print(total_views)
        #print('@@@@@@@@@')
        total_views=convertnumber(total_views)    
        #print(' location : ',location)
        #print("total_views",total_views)
        #print(total_views)
        quora_profile_information['total_views']=total_views
        nbanswers=0
        nbquestions=0
        nbfollowers=0
        nbfollowing=0
        #print('trying to get answers stats')
        try:
            html_source = browser.page_source
            source_soup = BeautifulSoup(html_source,"html.parser")
            # Find user social attributes : #answers, #questions, #shares, #posts, #blogs, #followers, #following, #topics, #edits
            nbanswers=browser.find_element_by_xpath("//div[contains(@class,'q-text qu-medium') and text()[contains(.,'Answer')]]")
            nbanswers=nbanswers.text.strip('Answers').strip().replace(',','')
            nbquestions =browser.find_element_by_xpath("//div[contains(@class,'q-text qu-medium') and text()[contains(.,'Question')]]")
            nbquestions=nbquestions.text.strip('Questions').strip().replace(',','')
            #print("questions ",nbquestions)
            nbfollowers= browser.find_element_by_xpath("//div[contains(@class,'q-text qu-medium') and text()[contains(.,'Follower')]]")
            nbfollowers=nbfollowers.text.strip('Followers').strip().replace(',','')
            #print("followers ",nbfollowers)
            nbfollowing= browser.find_element_by_xpath("//div[contains(@class,'q-text qu-medium') and text()[contains(.,'Following')]]")
            nbfollowing = nbfollowing.text.strip('Following').strip().replace(',','')
            #print("following ",nbfollowing)
        except Exception as ea:
            # print('cant get profile attributes answers quesitons followers following')
            # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ea).__name__, ea)
            time.sleep(1)
            if nbanswers==0:
                print(' User does not exists or does not have answers...')
                continue

        print('nb answers',nbanswers)
        # Open User profile file (save file)
        pathlib.Path('Users').mkdir(parents=True, exist_ok=True)
        save_path= Path.cwd() / Path("Users")
        save_file= save_path /  str( user_id + '.txt')
        file_user_profile = open(save_file, "w", encoding="utf8")
        quora_profile_information['user_id'] = user_id

        # writing answers stats to file
        quora_profile_information['nb_answers']=nbanswers
        quora_profile_information['nb_questions']=nbquestions
        quora_profile_information['nb_followers']=nbfollowers
        quora_profile_information['nb_following']=nbfollowing
        json.dump(quora_profile_information,file_user_profile)
        file_user_profile.write('\n')
        print('user has ', nbanswers,' amswers')
        # scroll down profile for loading all answers
        repeat=False
        if int(nbanswers)>30:
            repeat=True
        if int(nbanswers)>9:
            scrolldown(browser,repeat)
        # get answers text (we click on (more) button of each answer)
        if int(nbanswers)>0:
            #print('scrolling down for answers collect')
            i=0
            # Find and click on all (more)  to load full text of answers
            more_button = browser.find_elements_by_xpath("//div[contains(text(), '(more)')]")
            #print('nb more buttons',len(more_button))
            for jk in range(0,len(more_button)):
                ActionChains(browser).move_to_element(more_button[jk]).click(more_button[jk]).perform()
                time.sleep(1)
            try:
                questions_and_dates_tags= browser.find_elements_by_xpath("//a[@class='q-box qu-cursor--pointer qu-hover--textDecoration--underline' and contains(@href,'/answer/') and not(contains(@href,'/comment/')) and not(contains(@style,'font-style: normal')) ]")
                questions_link=[]
                questions_date=[]
                #filtering only unique questions and dates
                for QD in questions_and_dates_tags:
                    Qlink= QD.get_attribute("href").split('/')[3]
                    if Qlink not in questions_link:
                        questions_link.append(Qlink)
                        questions_date.append(QD.get_attribute("text"))

                questions_date=[convertDateFormat(d) for d in questions_date]
                answersText = browser.find_elements_by_xpath("//div[@class='q-relative spacing_log_answer_content']")
                answersText=[' '.join(answer.text.split('\n')[:]).replace('\r', '').replace('\t', '').strip() for answer in answersText]
            except Exception as eans:
                print('cant get answers')
                # print (eans)
                # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(eans).__name__, eans)
                continue
            # writing down answers ( date+ Question-ID + Answer text)
            for ind in range(0,int(nbanswers)):
                try:
                    #print(ind)
                    file_user_profile.write(questions_date[ind] +'\t' + questions_link[ind] + '\t' + answersText[ind] + '\n')
                except Exception as ew:
                    # print(ew)
                    # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ew).__name__, ew)
                    print('could not write to file...')
                    continue
        file_user_profile.close()
    browser.quit()
