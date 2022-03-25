import requests
from bs4 import BeautifulSoup
import pandas as pd


# Create an URL object
url = input('From which website would you like to extract a table? Please type the url.\n')
# Create object page
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

# first we need to find the table location. We do this by inspecting the page.
# Obtain information from tag <table>
table = input('In order to extract the table from the website we first need to identify the table´s location. '
              'In order to do so please type in the table´s class from the tag <table>.\n ')

table1 = soup.find('table', class_=str(table))

# inspecting the location of each column
# Obtain every title of columns with tag <th>

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

mydata.to_excel('test.xlsx')