# __main__.py
DEBUG = 1
import argparse
import json
import os
import pathlib
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import dateparser
import userpaths
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

from shared import \
	scrolldown, \
	show_more_of_articles, \
	view_more_comments, \
	view_more_replies, \
	view_collapsed_comments, \
	expand_hidden_comments, \
	show_more_of_comments, \
	connectchrome


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
# Users profile crawler
def users(users_list,save_path):
	browser= connectchrome()

	browser.maximize_window()
	browser.set_window_position(70, 0, windowHandle ='current')

	user_index=-1
	loop_limit=len(users_list)
	print('Starting the users crawling...')
	while True:
		print('_______________________________________________________________')
		user_index+=1
		if user_index >=loop_limit:
			print('Crawling completed, answers have been saved to  :  ', save_path)
			browser.quit()
			break
		# a dict to contain information about profile 
		quora_profile_information=dict()
		current_line= users_list[user_index].strip()
		current_line=current_line.replace('http', 'https')
		# we change proxy and sleep every 200 request (number can be changed)
		# sleep every while in order to not get banned
		if user_index % 5 == 4:
			sleep_time = (round(random.uniform(5, 10), 1))
			# print('*********')
			# print('Seleeping the browser for ', sleep_time)
			# print('*********')
			time.sleep(sleep_time)
		user_id=current_line.strip().replace('\r', '').replace('\n', '')
		url= "https://www.quora.com/profile/"+user_id
		print('processing quora user number : ', user_index +1, '	', url)
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
			nbanswers=browser.find_element_by_xpath("//div[text()[contains(.,'Answers')]]")
			nbanswers=nbanswers.text.strip('Answers').strip().replace(',','')
			nbquestions =browser.find_element_by_xpath("//div[text()[contains(.,'Questions')]]")
			nbquestions=nbquestions.text.strip('Questions').strip().replace(',','')
			#print("questions ",nbquestions)
			nbfollowers= browser.find_element_by_xpath("//div[text()[contains(.,'Followers')]]")
			nbfollowers=nbfollowers.text.strip('Followers').strip().replace(',','')
			#print("followers ",nbfollowers)
			# 'More' dropdown
			more_button= browser.find_element_by_xpath("//div[text()[contains(., 'More')]]/following-sibling::div[contains(@class, 'q-flex')]")
			if more_button:
				more_button.click()
			nbfollowing = browser.find_element_by_xpath("//div[text()[contains(.,'Following')]]")
			nbfollowing = nbfollowing.text.strip('Following').strip().replace(',','')
			#print("following ",nbfollowing)
		except Exception as ea:
			# print('cant get profile attributes answers quesitons followers following')
			# print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ea).__name__, ea)
			time.sleep(1)
			if nbanswers==0:
				print(' User does not exists or does not have answers...')
				continue

		# Open User profile file (save file)
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
		
		# scroll down profile for loading all answers
		print('user has ', nbanswers,' answers')
		if int(nbanswers)>9:
			# print('scrolling down for answers collect')
			scrolldown(browser)
		if int(nbanswers)>0:
			def click_on_all(find, selector):
				while True:
					buttons = find(selector)
					if not buttons:
						break
					for button in range(0, len(buttons)):
						ActionChains(browser).move_to_element(buttons[button]).click(buttons[button]).perform()
						time.sleep(0.5)

			show_more_of_articles(browser)
			view_more_comments(browser)
			view_more_replies(browser)
			view_collapsed_comments(browser)
			expand_hidden_comments(browser)
			show_more_of_comments(browser)

			# get answers text (we click on (more) button of each answer)
			# Find and click on all (more)  to load full text of answers
			# more_button = browser.find_elements_by_xpath("//div[contains(text(), '(more)')]")
			# #print('nb more buttons',len(more_button))
			# for jk in range(0,len(more_button)):
			# 	ActionChains(browser).move_to_element(more_button[jk]).click(more_button[jk]).perform()
			# 	time.sleep(1)
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
				print (eans)
				print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(eans).__name__, eans)
				continue
			# writing down answers ( date+ Question-ID + Answer text)
			for ind in range(0,int(nbanswers)):
				try:
					#print(ind)
					file_user_profile.write(questions_date[ind] +'\t' + questions_link[ind].rstrip()	 + '\t' + answersText[ind].rstrip() + '\n')
				except Exception as ew:
					# print(ew)
					# print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ew).__name__, ew)
					print('could not write to file...')
					continue
		file_user_profile.close()
		
	browser.quit()

# -------------------------------------------------------------
# -------------------------------------------------------------
def main():
	start_time = datetime.now()
	
	# Input Folder 
	input_path = Path(userpaths.get_my_documents()) / "QuoraScraperData" / "input"	
	pathlib.Path(input_path).mkdir(parents=True, exist_ok=True)
	
	# Read arguments
	parser=argparse.ArgumentParser()
	parser.add_argument("module", choices=['questions', 'answers', 'users'],help="type of crawler")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-f","--verbose",action="store_true",help="input keywords file path ")
	group.add_argument("-l","--quiet",action="store_true",help="input keywords list")
	parser.add_argument("input", help=" Input filepath or input list")
	parser.add_argument("-i","--index", type=int, default=0,help="index from which to start scraping ")
	args=parser.parse_args()
	
	# set starting crawl index
	list_index = args.index
	
	# set input list for crawling
	# if input is filepath
	keywords_list=[]
	if args.verbose:	
		filename=args.input
		print("Input file is : ", filename)
		if os.path.isfile(filename):
			with  open(filename, mode='r', encoding='utf-8') as keywords_file:
				keywords_list = keywords_file.readlines()
		elif os.path.isfile(Path(input_path) / filename):
			with  open(Path(input_path) / filename, mode='r', encoding='utf-8') as keywords_file:
				keywords_list = keywords_file.readlines()
		else:
			print()
			print("Reading file error: Please put the file in the program directory: ",Path.cwd() ," or in the QuoraScraperData folder :",input_path ,"  and try again")
			print()
	
	# if input is list
	elif args.quiet:
		keywords_list = [item.strip() for item in args.input.strip('[]').split(',')]
	
	keywords_list=keywords_list[list_index:]
   
	#create ouptut folder
	module_name=args.module
	save_path = Path(userpaths.get_my_documents()) / "QuoraScraperData" / module_name
	pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
	
	# launch scraper
	# if module_name.strip()=='questions':
	# 	questions(keywords_list,save_path)
	# elif module_name.strip() == 'answers':
	# 	answers(keywords_list,save_path)
	# elif module_name.strip() == 'users':
	users(keywords_list,save_path)
	
	end_time = datetime.now()
	print(' Crawling tooks a total time of  : ',end_time-start_time)

if __name__ == '__main__': main()
