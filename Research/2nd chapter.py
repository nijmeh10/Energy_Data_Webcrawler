from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bs = BeautifulSoup(html, "html.parser")
nameList = bs.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())

numberPrince = bs.findAll(text = 'the prince')
print(len(numberPrince))

title = bs.findAll(id = 'title')
print(title)

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bs = BeautifulSoup(html, 'html.parser')

for child in bs.find('table', {'id': 'giftList'}).children:
    print(child)

for sibling in bs.find('table', {'id':'giftList'}).tr.next_siblings:
    print(sibling)
