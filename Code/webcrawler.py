from bs4 import BeautifulSoup
import requests
import os
import sys


class Content:
    """
    Common base class for all articles/pages
    """

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """
        Flexible printing function controls output
        """
        print('New article found for topic: {}'.format(self.topic))
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))


class Website:
    """Contains information about website structure"""

    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:

    def __init__(self):
        self.main_menu()

    def main_menu(self):
        """
        Provides the webcrawler's main menu.
        """
        self.clear_screen()
        print('\n'+'*' * 80)
        print('Webcrawler')
        print('*' * 80)
        print('\nPlease select one of the following commands: ')
        print('\t1. Extract links from a website')
        print('\t2. Extract a table from a website')
        print('\t3. Extract text from a website')
        print('\t4. Exit')
        selection = input('Please type: 1, 2, 3, or 4 ')
        if selection == '1':
            pass
        elif selection == '2':
            pass
            self.main_menu()
        elif selection == '3':
            pass
            self.main_menu()
        elif selection == '4':
            pass
            self.exit()
        else:
            self.wrong_input()
            self.main_menu()

    def clear_screen(self):
        """
        Clears the screen if user goes back to menu.
        """
        # For mac and linux os.name is 'posix'.
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            _ = os.system('cls')

    def wrong_input(self, message=''):
        print(message)
        input('Invalid input. Please press enter to continue. ')

    def exit(self):
        """
        Cleans up resources and exits the webcrawler.
        """
        print('\nExiting Webcrawler - good bye!')
        sys.exit()

    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        """
        Utilty function used to get a content string from a Beautiful Soup
        object and a selector. Returns an empty string if no object
        is found for the given selector
        """
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        return ''

    def search(self, topic, site):
        """
        Searches a given website for a given topic and records all pages found
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs['href']
            # Check to see whether it's a relative or an absolute URL
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print('Something was wrong with that page or URL. Skipping!')
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()


crawler = Crawler()



siteData = [
    ['O\'Reilly Media', 'http://oreilly.com', 'https://ssearch.oreilly.com/?q=',
        'article.product-result', 'p.title a', True, 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com', 'http://www.reuters.com/search/news?blob=', 'div.search-result-content',
        'h3.search-result-title a', False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu', 'https://www.brookings.edu/search/?s=',
        'div.list-content article', 'h4.title a', True, 'h1', 'div.post-body']
]
sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2],
                         row[3], row[4], row[5], row[6], row[7]))

topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)
