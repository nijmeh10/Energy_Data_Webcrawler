from selenium import webdriver
import pandas as pd

# Copy path to Chrome
browser = webdriver.Chrome("D:/Ricarda/Dokumente/Studium/Hochschule Düsseldorf/4. Semester/Thesis/Code/"
                           "Energy_Data_Webcrawler/chromedriver_win32/chromedriver.exe")

# Determine a website
url = "https://en.wikipedia.org/wiki/List_of_best-selling_books#More_than_100_million_copies"
# Open the website in the automated chrome version
browser.get(url)
# Read the Text on the website
text_website = browser.page_source
df = pd.read_html(text_website)
print(df)
