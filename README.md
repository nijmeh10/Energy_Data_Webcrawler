# Web crawler
Web crawlers are also called searchbots, spiders or robots. The term refers to a computer program that is able to automatically search the Internet for specific information and data. The data can then be evaluated, sorted according to specified criteria and stored. 
This web crawler is used to extract data and information related to energy. 


## xx. Business understanding 
*This section focuses on understanding the business question and identifying the relevant objectives and requirements for implementing a webcrawler.*

**In a nutshell: Implementation of a web crawler capable of extracting data from websites, especially energy data.**

### Libraries 📚
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
  - With colorama, text on the console can be colored, which can increase the readability in some places.

####Installation of libraries####
Some libraries require installation via the command prompt and cannot be installed just by fulfilling the requirements in the requirements.txt file. The following steps show how to install such libraries.
- **BeautifulSoup4:** 
  - pip install beautifulsoup4
- **urllib.request**
  - pip install urllib


### Functions 🧰
- **get_any_table**: here it is important to know the location of each part of the table. In some cases it might me necessary to adapt the code, e.g. when the column's tag is not <th>.
