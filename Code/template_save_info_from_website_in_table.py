from bs4 import BeautifulSoup
import requests
import pandas as pd

# Using this you can create tables from website information and converting this to csv

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

#print(name)
#print(price)
#print(reviews)
#print(description)

#price1 = soup.find('h4', class_='pull-right price')
#print(price1.text)

# Create for loop to make string from find_all list
product_name_list = []
for i in name:
    name = i.text
    product_name_list.append(name)
price_list = []

for i in price:
    price = i.text
    price_list.append(price)
review_list = []

for i in reviews:
    rev = i.text
    review_list.append(rev)

description_list = []
for i in description:
    desc = i.text
    description_list.append(desc)

# Create dataframe

table = pd.DataFrame({'Product Name': product_name_list, 'Price': price_list, 'Reviews': review_list, 'Description':
    description_list})

#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(table)
table.to_excel('table.xlsx')

