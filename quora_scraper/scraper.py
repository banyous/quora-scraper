# __main__.py
import  sys
import datetime
from .questions_url_scraper import questions
from .answers_scraper import answers
from .users_scraper import users

def main():
    # start time
    start_time = datetime.datetime.now()
    list_index=0
    # we accept only 3 or 4 sys arguments
    nb_arguments= len(sys.argv)
    if  nb_arguments < 4 or nb_arguments >5:
        print('Error: Please make sure to provide the correct input parameters: -k or -f, plus keywords list or file ')
        sys.exit()
    elif nb_arguments == 5:
        list_index = sys.argv[4]
    module_name=sys.argv[1]
    param = sys.argv[2]
    items=sys.argv[3]
    if module_name.strip().lower()=='questions':
        questions(param, items,list_index)
    if module_name.strip().lower() == 'answers':
        answers(param, items, list_index)
    if module_name.strip().lower() == 'users':
        users(param, items, list_index)

    # finish time
    end_time = datetime.datetime.now()
    print(' Crawling tooks a total time of  : ',end_time-start_time)

if __name__ == '__main__': main()
