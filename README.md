# Web crawler
Web crawlers are also called searchbots, spiders or robots. The term refers to a computer program that is able to automatically search the Internet for specific information and data. The data can then be evaluated, sorted according to specified criteria and stored. 
This web crawler is used to extract data and information related to energy. 


## xx. Business understanding 
*This section focuses on understanding the business question and identifying the relevant objectives and requirements for implementing a webcrawler.*

**In a nutshell: Implementation of a web crawler capable of extracting data from websites, especially energy data.**

### Libraries
In the requirements.txt file you will find all the libraries that I used for the project. The most important libraries are briefly described below:
- **BeautifulSoup4: extract website information** 
  - Beautiful Soup enables the user to extract information from web pages. It relies on an HTML or XML parser and provides Pythonic idioms for iterating, searching and modifying the parse tree.
- **requests: asking for permission from the hosting server**
  - IT obtains the hosting server's permission if we want to retrieve data from its website
  - If the output is <Response [200]> so that means the server allows us to collect data from their website. 
- **pandas: creating a dataframe**
  - Pandas is used to create a data frame in the form of a table for downloaded data.
- **lxml: changing the HTML format into a Python-friendly format**
  - The lxml library helps to process HTML in the Python programming language.
- **urllib.request: handling URLs**
  - It is used for retrieving URLs (Uniform Resource Locators). Using the urlopen function, it can retrieve URLs over a variety of different protocols.
- **colorama: providing colored text output**
  - With colorama, text on the console can be colored, which increases the readability.

##Installation of libraries##
Some libraries require installation via the command prompt and cannot be installed just by fulfilling the requirements in the requirements.txt file. The following steps show how to install such libraries.
1. **BeautifulSoup4:** 
  - Windows: open your command prompt and type the following command
    - pip install beautifulsoup4
2. **urllib.request**
  - Windows: open your command prompt and type the following command
    - pip install urllib


### Classes
- **Class "Crawler": Allows the user to navigate through a main menu where he/she can choose one of the following options:**
  1. Test whether the website you want to crawl allows web crawling: Web scraping is not illegal per se, but the problem is when it is used without the permission of the website owner and in violation of the terms of use. Therefore, before crawling a website, it is important to obtain permission from the hosting server to retrieve data from its website. 
  2. Extract links from a website: Allows the user to extract both external and internal links from a website. These are then displayed in an Excel file and saved under the Data/links folder.
  3. Extract a table from a website: This function is suitable for downloading tables from websites. The data of the table is displayed in an Excel file, which is then saved under Data/tables.
  4. Extract text from a website: Allows the user to download the text of a website.
  5. Extract images from a website: Allows the user to download all images from a website.
  6. Exit: stops the web crawler.
- **Class "Content"**
- **Class "Website"**


### Functions 
- **get_any_table**: 
  - here it is important to know the location of each part of the table. In some cases it might me necessary to adapt the code, e.g. when the column's tag is not <th>.
