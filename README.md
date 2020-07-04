# Quora-scraper

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://github.com/banyous/quora-scraper)


Quora-scraper is a command-line application written in Python that scrapes Quora data. It simulates a browser environment to let you scrape Quora rich textual data. You can use one of the three scraping modules to: Find questions that discuss about certain topics (such as Finance, Politics, Tesla or Donald-Trump). Scrape Quora answers related to certain questions, or scrape users profile. Please use it responsibly ! 

## Install
To use our scraper, please follow the steps below:
- Install python 3.6 or upper versions.
- Install the latest version of google-chrome.
- Download chromedriver and add it to your sys path:  https://sites.google.com/a/chromium.org/chromedriver/home 
- Install quora-scraper:

```sh
$ pip install quora-scraper
```
To update quora-scraper:

```sh
$ pip install quora-scraper --upgrade
```

Alternatively, you can clone the project and run the following command to install: Make sure you cd into the quora-scraper folder before performing the command below.

```sh
$  python setup.py install
```

## Usage

quora-scraper has three scraping modules : ```questions``` ,```answers```,```users```.
#### 1) Scraping questions URL:

You can scrape questions related to certain topics using ```questions``` command. This module takes as an input a list of topic keywords. Output is a questions_URL file containing the topic's question links. 

Scraping a topic questions can be done as follows:

- a) Use -l parameter + topic keywords list.

    ```sh
    $ quora-scraper questions -l [finance,politics,Donald-Trump]
    ```

- b) Use -f parameter + topic keywords file location. (keywords must be line separated inside the file):

    ```sh
    $ quora-scraper questions -f  topics_file.txt
    ```
    
#### 2) Scraping answers:

Quora answers are scraped using ```answers``` command. This module takes as an input a list of Questions URL. Output is a file of scraped answers (answers.txt). An answer consists of :

Quest-ID | AnswerDate | AnswerAuthor-ID | Quest-tags | Answer-Text 

To scrape answers, use one of the following methods:

- a) Use -l parameter + question URLs list. 

    ```sh
    $ quora-scraper answers -l [https://www.quora.com/Is-milk-good,https://www.quora.com/Was-Einstein-a-fake-and-a-plagiarist]
    ```

- b)  Use -f parameter + question URLs file location:
 
    ```sh
    $ quora-scraper answers -f  questions_url.txt
    ```
 
#### 3) Scraping Quora user profile:

You can scrape Quora Users profile using ```users``` command. The users module takes as an input a list of Quora user IDs. The output is UserProfile file containing:

First line :
UserID | ProfileDescription |ProfileBio | Location | TotalViews |NBAnswers | NBQuestions | NBFollowers |  NBFollowing

Remaining lines (User's answers):
AnswerDate | QuestionID | AnswerText 

Scraping Users profile can be done as follows:

- a) Use -l parameter + User-IDs list. 
    ```sh
    $ quora-scraper users -l [Albert-Einstein-195,Jackie-Chan-8]
    ```
   
- b)  Use -f parameter + User-IDs file. 

    ```sh
    $ quora-scraper users -f quora_username_file.txt
    ```

### Notes
a) Input files must be line separated.

b) Output files fields are tab separated.

c) You can add a list/line index parameter In order to start the scraping from that index. The code below will start scraping from "physics" keyword:
    ```sh
    $ quora-scraper questions -l [finance,politics,tech,physics,life,sports]  -i 3
    ```
d) Quora website puts limit on the number of questions accessible on a topic page. Thus, even if a topic has a large number of questions (ex: 100k), the number scraped questions links will not exceed 2k or 3k questions.
 
e) For more help use : 
 ```sh
    $ quora-scraper --help
 ```
f) Quora-scraper uses  xpaths and bs4 methods to scrape Quora webpage elements. Since Quora HTML Structure is constantly changing, the code may need modification from time to time. Please feel free to update and contribute to the source-code in order to keep the scraper up-to-date.
     
  
License
----

This project uses the following license: [MIT]




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [MIT]: <https://github.com/banyousr>

