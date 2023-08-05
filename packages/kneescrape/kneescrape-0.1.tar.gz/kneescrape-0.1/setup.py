from setuptools import setup

setup(
	name = "kneescrape",
	version = "0.1",
	author = "Jakob Svanholm",
	author_email = "jakob@rymdlego.se",
	url = "https://github.com/rymdlego/kneescrape",
	description = "A simple script to crawl a website and scrape for emails and unique words to create relevant dictionary.",
	keywords = "crawl osint wordlist infosec",
	scripts=['kneescrape'],
	install_requires=['docopt', 'requests', 'bs4', 'lxml', 're']
)
