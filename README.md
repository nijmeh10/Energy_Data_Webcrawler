# Web crawler
Web crawlers are also called searchbots, spiders or robots. The term refers to a computer program that is able to automatically search the Internet for specific information and data. The data can then be evaluated, sorted according to specified criteria and stored. This web crawler is used to extract data and information related to energy. 


## xx. Business understanding 
*This section focuses on understanding the business question and identifying the relevant objectives and requirements for implementing a webcrawler.*

**In a nutshell: Implementation of a web crawler capable of extracting data from websites, especially energy data.**

### Libraries 📚
In the requirements.txt file you will find all the libraries that I used for the project. The most important libraries are briefly described below:
- **BeautifulSoup4:** 
- **requests: asking permission from the hosting server if we want to fetch data from their website**
  - If the output is <Response [200]> so that means the server allows us to collect data from their website. 
- **pandas: creating a dataframe**
- **lxml: changing the HTML format into a Python-friendly format**

### Functions 🧰
- **get_any_table**: here it is important to know the location of each part of the table. In some cases it might me necessary to adapt the code, e.g. when the column's tag is not <th>.
