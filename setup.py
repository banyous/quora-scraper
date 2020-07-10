from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
    
    
    
setup(
  name = 'quora-scraper',
  packages = ['quora_scraper'],
  version = '1.1.0',
  license='MIT',
  description = "Python based code to scrap and download data from quora website: questions related to certain topics, answers given on certain questions and users profile data",
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Youcef Benkhedda',
  author_email = 'y_benkhedda@esi.dz',
  url="https://github.com/banyous/quora-scraper",
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['quora', 'topics', 'Q&A','user','scraper', 'download','answers','questions'],
  include_package_data=True,
  install_requires=[
			'selenium',
			'bs4',
			'webdriver-manager',
			'dateparser',
			'userpaths'
      ],
  entry_points={
	"console_scripts": [
	    "quora-scraper=quora_scraper.scraper:main",
        ]
    },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
  
)
