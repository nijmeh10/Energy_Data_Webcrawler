# Webcrawler

## Automated Version of Chrome
1. Finding the current Chrome version I use by searching:https://chromedriver.storage.googleapis.com/LATEST_RELEASE
2. Found out I use version 98.0.4758.80
3. Download the automated version via https://chromedriver.chromium.org/downloads and selecting download for the Chrome version 98: https://chromedriver.storage.googleapis.com/index.html?path=98.0.4758.80/


### Libraries 📚
In the requirements.txt file you will find all the libraries that I used for the project. The most important libraries are briefly described below:
- **BeatifulSoup4:** 
- **requests: asking permission from the hosting server if we want to fetch data from their website**
  - If the output is <Response [200]> so that means the server allows us to collect data from their website. 
- **pandas: creating a dataframe**
- **lxml: changing the HTML format into a Python-friendly format**

### Functions 🧰
- **get_any_table**: here it is important to know the location of each part of the table. In some cases it might me necessary to adapt the code, e.g. when the column's tag is not <th>.
