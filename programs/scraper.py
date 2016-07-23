###this is a test...but could be modified for usefulness

from urllib import urlopen
from bs4 import BeautifulSoup
import re

test= urlopen("http://google.com")
bsOnj2=BeautifulSoup(test)
print(bsOnj2)

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id ="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])        
    except AttributeError:
        print("This page is missing something! No worries though!")
        
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
               #We have encountered a new page
                newPage = link.attrs['href']
                print("----------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")

test= urlopen("http://google.com") #you can test out scraper to ensure you are connecting
bsOnj2=BeautifulSoup(test)
print(bsOnj2)
