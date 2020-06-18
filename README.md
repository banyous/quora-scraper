# Quora-scraper

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://github.com/banyous/Quora-and-Twitter-crawler-and-user-matcher)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/banyous/Quora-and-Twitter-crawler-and-user-matcher)

Quora-scraper simulates a browser environment to let you scrape Quora rich textual data. You can use one of the three scraping modules to: Find questions that discuss about certain topics (such as Finance, Politics, Tesla or Donald-Trump). Scrape Quora answers related to certain question(s), or scrape users profile.


## Install
To use our scraper, please follow the steps below:
- install the latest version of google-chrome.
- install python 3.6 or upper versions.
- download chromedriver and add it to your sys path:  https://sites.google.com/a/chromium.org/chromedriver/home 
- install quora-scraper:

```sh
$ pip install quora-scraper
```
To update quora-scraper:

```sh
$ pip install quora-scraper --upgrade
```


## Usage

quora-scraper has three scraping modules : ```questions``` ,```answers```,```users```.
#### 1) Scraping questions URL:

You can scrape questions related to certain topics using ```questions``` command. This module takes as an input a list of topic keywords. Output is a questions_URL file for each topic saved under QuestionsURLs/ directory. 

Scraping a topic questions can be done as follows:

- a) Use "-k" parameter + topic keywords list.

    ```sh
    $ quora-scraper questions -k [finance,politics,Donald-Trump]
    ```

- b) Use "-f" parameter + topic keywords file location. (keywords must be line separated inside the file):

    ```sh
    $ quora-scraper questions -f  topics_file.txt
    ```
    
#### 2) Scraping answers:

Quora answers are scraped using ```answers``` command. This module takes as an input a list of Questions URL. Output is a file of scraped answers (answers.txt). Each answer consists of :

Quest-ID | AnswerDate | AnswerAuthor-ID | Quest-tags | Answer-Text 

Scraping answers can be done as follows:

- a) Use "-k" parameter + question URLs list. 

    ```sh
    $ quora-scraper answers -k [https://www.quora.com/Is-milk-good,https://www.quora.com/Was-Einstein-a-fake-and-a-plagiarist]
    ```

- b)  Use "-f" parameter + question URLs file location:
 
    ```sh
    $ quora-scraper answers -f  questions_url.txt
    ```
 
#### 3) Scraping Quora user profile:

You can scrap Quora Users profile using ```users``` command. This module takes as an input a list of Quora user IDs. Output is UserProfile file for eah UserID saved under the Qusers/ directory, Users data consists of :

First line :
UserID | ProfileDescription |ProfileBio | Location | TotalViews |NBAnswers | NBQuestions | NBFollowers |  NBFollowing

Remaining lines (User's answers):
AnswerDate | QuestionID | AnswerText 

Scraping Users profile can be done as follows:

- a) Use "-k" parameter + User-IDs list. 
    ```sh
    $ quora-scraper users -k [Albert-Einstein-195,Jackie-Chan-8]
    ```
   
- b)  Use "-f" parameter + User-IDs file. 

    ```sh
    $ quora-scraper users -f quora_username_file.txt
    ```

### Note 
a) Please note that all output files have tab separated fields.

b) You can add a list/line index parameter In order to start the scraping from that index. The code below will start scraping from "physics" keyword:
    ```sh
    $ quora-scraper questions -k [finance,politics,tech,physics,life,sports] 3
    ```
 
c) Quora-scraper is a command-line application written in Python that scrapes Quora data. It uses  xpaths method to scrap Quora webpage elements. Since Quora HTML Structure is constantly changing, the code may need modification from time to time. Please feel free to update and contribute to the source-code in order to keep the scraper up-to-date.


License
----

This project uses the following license: [MIT]




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [MIT]: <https://github.com/banyousr>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>

