from bs4 import BeautifulSoup
import requests


# Define URL
url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
# Ask hosting server to fetch url
requests.get(url)

pages = requests.get(url)
#print(pages)

# parser-lxml = Change html to Python friendly format
soup = BeautifulSoup(pages.text, 'lxml')
#print(soup)

# Access h1 tag
#print(soup.header)
#print(soup.header.p.string)

# Access ‘a’ tag in <header>
a_start = soup.header.a
#print(a_start)
# Access only the attributes using attrs
#print(a_start.attrs)
#print(a_start['data-target'])
#a_start['new attribute'] = 'This is the new attribute'
#print(a_start.attrs)

#print(soup.header.div)

# Searching specific attributes of tags
#print(soup.find('h4', class_= 'pull-right price'))
# Using find_all
#print(soup.find_all('h4', class_= 'pull-right price'))
# Slicing the results of find_all
#print(soup.find_all('h4', class_= 'pull-right price')[2:5])

# Using filter to find multiple tags
#print(soup.find_all(['h4', 'a', 'p']))
#soup.find_all(['header', 'div'])
#print(soup.find_all(id = True)) # class and id are special attribute so it can be written like this
#print(soup.find_all(class_= True))


# Filter by name
name = soup.find_all('a', class_='title')
# Filter by price
price = soup.find_all('h4', class_ = 'pull-right price')
# Filter by reviews
reviews = soup.find_all('p', class_ = 'pull-right')
# Filter by description
description = soup.find_all('p', class_ ='description')