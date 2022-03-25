from bs4 import BeautifulSoup
import requests

# Create an URL object
url = input('From which website would you like to extract a table? Please type the url.\n')
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

print(soup.table.attrs)
