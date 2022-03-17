from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

#random.seed(datetime.datetime.now())


#def getLinks(articleUrl):
#    html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
#    bs = BeautifulSoup(html, 'html.parser')
#    return bs.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))


#links = getLinks('/wiki/Kevin_Bacon')
#while len(links) > 0:
#    newArticle = links[random.randint(0, len(links)-1)].attrs['href']
#    print(newArticle)
#    links = getLinks(newArticle)

#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#import re

#pages = set()


#def getLinks(pageUrl):
#    global pages
#    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
#    bs = BeautifulSoup(html, 'html.parser')
#    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
#        if 'href' in link.attrs:
#            if link.attrs['href'] not in pages:
#                #We have encountered a new page
#                newPage = link.attrs['href']
#                print(newPage)
#                pages.add(newPage)
#                getLinks(newPage)
#getLinks('')

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('This page is missing something! Continuing.')

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # We have encountered a new page
                newPage = link.attrs['href']
                print('-' * 20)
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks('')