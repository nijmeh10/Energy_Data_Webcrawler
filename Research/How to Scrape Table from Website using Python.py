import requests
from bs4 import BeautifulSoup
import pandas as pd


# Create an URL object
url = 'https://www.worldometers.info/coronavirus/'
# Create object page
page = requests.get(url)
#print(page)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')
#print(soup)

# first we need to find the table location. We do this by inspecting the page.
# Obtain information from tag <table>
table1 = soup.find('table', id='main_table_countries_today')
# inspecting the location of each column
# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
print(headers)
# Convert wrapped text in column 13 into one line text
headers[13] = 'Tests/1M pop'
print(headers)

# Create a dataframe
mydata = pd.DataFrame(columns=headers)
# Create a for loop to fill mydata
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

#mydata.to_excel('cases.xlsx')

# Drop and clearing unnecessary rows
mydata.drop(mydata.index[0:7], inplace=True)
mydata.drop(mydata.index[222:229], inplace=True)
mydata.reset_index(inplace=True, drop=True)
# Drop “#” column
mydata.drop('#', inplace=True, axis=1)

mydata.to_excel('cases.xlsx')
