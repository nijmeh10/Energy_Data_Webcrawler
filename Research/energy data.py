from bs4 import BeautifulSoup
import requests
import pandas as pd



# Define URL
url = 'https://ec.europa.eu/eurostat/databrowser/view/NRG_PC_205__custom_1822321/default/table?lang=de'
# Ask hosting server to fetch url
requests.get(url)

pages = requests.get(url)
print(pages)