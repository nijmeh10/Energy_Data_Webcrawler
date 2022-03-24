import shutil
from bs4 import BeautifulSoup
import os
import sys
import requests
from urllib.parse import urlparse, urljoin
import colorama
import csv
from datetime import datetime

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
# Internal links are URLs that link to other pages of the same website.
# External links are URLs that link to other websites.
internal_urls = set()
external_urls = set()

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
    """
    Crawler...
    """

    def __init__(self):
        self.main_menu()

    def main_menu(self):
        """
        Provides the webcrawler's main menu.
        """
        self.clear_screen()
        print('\n'+'*' * 80)
        headline = 'Webcrawler'
        new_headline = headline.center(80)
        print(new_headline)
        print('*' * 80)
        print('\nPlease select one of the following commands: \n')
        print('\t1. Test whether the website you want to crawl allows webcrawling')
        print('\t2. Extract links from a website')
        print('\t3. Extract a table from a website')
        print('\t4. Extract text from a website')
        print('\t4. Exit\n')
        selection = input('Please type: 1, 2, 3, or 4 \n')
        if selection == '1':
            url = input('Before starting to crawl website it is necessary to test whether the server allows us to '
                        'collect data from their website. Which website would you like to test? Please type the url.\n')
            requests.get(url)
            page = str(requests.get(url))
            if page == '<Response [200]>':
                print('This is a safe website, you can start webcrawling now.')
            else:
                print('I am sorry, you are not allowed to crawl this website. Try another one.')
            self.main_menu()
        elif selection == '2':
            webpage = input('From which website do you want to extract your links? \n')
            self.get_all_website_links(webpage)
        elif selection == '3':
            pass
            self.main_menu()
        elif selection == '4':
            pass
            self.main_menu()
        elif selection == '5':
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

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_website_links(self, url):
        """
        Returns all URLs that is found on `url` in which it belongs to the same website.
        Additionally enables the user to create a csv file containing the links.
        """
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue

            # join the URL if it's relative (not absolute link)
            href = urljoin(url, href)

            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            if not self.is_valid(href):
                # not a valid URL
                continue
            if href in internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
                if href not in external_urls:
                    print(f"{GRAY}[!] External link: {href}{RESET}")
                    external_urls.add(href)
                continue
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            urls.add(href)
            internal_urls.add(href)
        print("[+] Total Internal links:", len(internal_urls))
        print("[+] Total External links:", len(external_urls))
        print("[+] Total URLs:", len(external_urls) + len(internal_urls))

        IL = list(internal_urls)
        EL = list(external_urls)

        selection = input('\nWould you like to save the links in a csv file? Please type "yes" or "no". \n')
        if selection == 'yes':
            with open('Links.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Internal links'])
                writer.writerow(IL)
                writer.writerow('\n')
                writer.writerow(['External links'])
                writer.writerow(EL)
            time = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
            new_filename = time
            shutil.move(f'Links.csv', f'..\\Data\\links\\{new_filename}.csv')
            print(f'Your file "{new_filename}" has been saved to the directory "Data/links". '
                  f'\nReturning back to the main menu. \n')
            self.main_menu()
        elif selection == 'no':
            print('Okay. Returning back to the main menu. ')
            self.main_menu()
        else:
            self.wrong_input()
            self.main_menu()












