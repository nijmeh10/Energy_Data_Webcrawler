import os
import csv
import sys
import shutil
import colorama
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


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
        print('\t1. Test whether the website you want to crawl allows web crawling')
        print('\t2. Extract links from a website')
        print('\t3. Extract a table from a website')
        print('\t4. Extract text from a website')
        print('\t5. Extract images from a website')
        print('\t6. Exit\n')
        selection = input('Please type: 1, 2, 3, 4, 5 or 6 \n')
        if selection == '1':
            url = input('Before starting to crawl website it is necessary to test whether the server allows us to '
                        'collect data from their website. Which website would you like to test? Please type the url.\n')
            requests.get(url)
            page = str(requests.get(url))
            if page == '<Response [200]>':
                print('This is a safe website, you can start web crawling now.')
            else:
                print('I am sorry, you are not allowed to crawl this website. Try another one.')
            self.main_menu()
        elif selection == '2':
            webpage = input('From which website do you want to extract your links? \n')
            self.get_all_website_links(webpage)
        elif selection == '3':
            url = input('From which website would you like to extract a table? Please type the url.\n')
            self.get_any_table(url)
            self.main_menu()
        elif selection == '4':
            url = input('From which website would you like to extract the text? Please type the url.\n')
            self.get_text(url)
            self.main_menu()
        elif selection == '5':
            url_base = input("Please type url you want to extract the images from:\n")
            folder_name = input("Please define the name of the folder where the pictures will be saved:\n")
            self.main(url_base, folder_name)
            shutil.move(f'{folder_name}', f'..\Data\images\{folder_name}')
            print('Your images have been saved to the directory "Data/images". ')
            self.main_menu()
        elif selection == '6':
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
        return bs(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        """
        Utility function used to get a content string from a Beautiful Soup
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
            if site.absoluteUrl:
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
        soup = bs(requests.get(url).content, "html.parser")

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

    def get_any_table(self, url):
        """
        Enables to download any table from any website and convert the information into an Excel-file
        """
        # Create object page
        page = requests.get(url)
        # Change html to Python friendly format and obtain page's information
        soup = bs(page.text, 'lxml')

        # first we need to find the table location. We do this by inspecting the page and obtaining the information
        # from tag <table>
        table = input('In order to extract the table from the website we first need to identify the table´s location.\n'
                      'In order to do so please type in the table´s class from the tag <table>.\n')

        table1 = soup.find('table', class_=str(table))

        # Inspecting the location of each column, this is in most cases the tag <th>
        # If this is not <th> this needs to be adapted here
        headers = []
        for i in table1.find_all('th'):
            title = i.text
            headers.append(title)

        # Create a dataframe
        mydata = pd.DataFrame(columns=headers)
        # Create a for loop to fill mydata
        for j in table1.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(mydata)
            mydata.loc[length] = row

        mydata.to_excel('any_table.xlsx')
        time = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
        new_filename = time
        shutil.move(f'any_table.xlsx', f'..\\Data\\tables\\{new_filename}.xlsx')
        print(f'\nYour file "{new_filename}" has been saved to the directory "Data/tables". '
              f'\nReturning back to the main menu. \n')

    def get_text(self, url):
        """
        Downloads the whole text from a website
        """
        html = urlopen(url).read()
        soup = bs(html, features="html.parser")

        # erase all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print(text)
        print('\nReturning back to the main menu. \n')

    def get_all_images(self, url):
        """
        Returns all image URLs on a single `url`
        """
        soup = bs(requests.get(url).content, "html.parser")

        urls = []
        for img in tqdm(soup.find_all("img"), "Extracting images"):
            img_url = img.attrs.get("src")
            if not img_url:
                # if img does not contain src attribute, just skip
                continue

            # make the URL absolute by joining domain with the URL that is just extracted
            img_url = urljoin(url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            # finally, if the url is valid
            if self.is_valid(img_url):
                urls.append(img_url)
        return urls

    def download(self, url, pathname):
        """
        Downloads a file given an URL and puts it in the folder `pathname`
        """
        # if path doesn't exist, make that path dir
        if not os.path.isdir(pathname):
            os.makedirs(pathname)
        # download the body of response by chunk, not immediately
        response = requests.get(url, stream=True)
        # get the total file size
        file_size = int(response.headers.get("Content-Length", 0))
        # get the file name
        filename = os.path.join(pathname, url.split("/")[-1])
        # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
        progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B",
                        unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for data in progress.iterable:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))


    def main(self, url, path):
        # get all images
        imgs = self.get_all_images(url)
        for img in imgs:
            # for each image, download it
            self.download(img, path)
