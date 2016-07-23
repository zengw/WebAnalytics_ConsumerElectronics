# -*- coding: utf-8 -*-
# Extracting and Parsing Web Site Data (Python)

# prepare for Python version 3x features and functions
from __future__ import division, print_function

# import packages for web scraping/parsing
import requests  # functions for interacting with web pages
from lxml import html  # functions for parsing HTML
from bs4 import BeautifulSoup  # DOM html manipulation

# -----------------------------------------------
# demo using the requests and lxml packages
# -----------------------------------------------
# test requests package on the home page for 'Good Morning Imperial Stout' 
    #by Tree House Brewing Company
web_page = requests.get('https://www.beeradvocate.com/beer/profile/28743/136936/?sort=topr&start=0')
# obtain the entire HTML text for the page of interest

# show the status of the page... should be 200 (no error)
web_page.status_code
# show the encoding of the page... should be utf8
web_page.encoding

# show the text including all of the HTML tags... lots of tags
web_page_text = web_page.text
print(web_page_text)

# parse the web text using html functions from lxml package
# store the text with HTML tree structure
web_page_html = html.fromstring(web_page_text)

# extract the text within paragraph tags using an lxml XPath query
web_page_content = web_page_html.xpath('//div/text()') 
# show the resulting text string object
print(web_page_content)  # has a few all-blank strings
print(len(web_page_content))
print(type(web_page_content))  # a list of character strings

# -----------------------------------------------------------
# demo of parsing HTML with beautiful soup instead of lxml
# -----------------------------------------------------------
my_soup = BeautifulSoup(web_page_text)
# note that my_soup is a BeautifulSoup object
print(type(my_soup))

# remove JavaScript code from Beautiful Soup page object
# using a comprehension approach
[x.extract() for x in my_soup.find_all('script')] 
print(my_soup)
# gather all the text from the paragraph tags within the object
# using another list comprehension 
soup_content = [x.text for x in my_soup.find_all('div')]
# show the resulting text string object
print(soup_content)  # note absense of all-blank strings
print(len(soup_content))  
print(type(soup_content))  # a list of character strings

# there are carriage return, line feed charachters, and spaces
# to delete from the text... but we have extracted the essential 

import os  # access to operating system commands
os.getcwd()  # shows location of current working directory
os.chdir('C:\\Users\\zking\\Documents\\School\\Predict 452\\Assignment 1\\wnds_chapter_3a_with_write')
my_file_object = open('good_morning.txt', 'w')  # opens file for writing
# convert soup_content to a sequence of strings and write to file
my_file_object.writelines(str(soup_content))  
my_file_object.close()  # close file so it can be used by other applications