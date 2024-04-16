
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

inpu = input("Enter the name of movie ")
inpu = inpu.split()
inp = ""
flag = 0
for i in inpu:
    if flag == 0:
        inp = inp + i
        flag = 1
    else:
        inp = inp + "+" + i
url = "https://www.imdb.com/find?q="+inp+"&ref_=nv_sr_sm"

caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = False
driver = webdriver.Firefox()
driver.get(url)
con = driver.page_source
s = BeautifulSoup(con, "html.parser")
print(s)
imdb_id = s.select_one('.ipc-metadata-list-summary-item__tc a')
n = imdb_id.attrs['href'].split('/')[2]
print(f"IMDb ID for {inp}: {n}")
print("Processing...")
next_page = "https://m.imdb.com/title/" + n + "/reviews?ref_=tt_urv"
print(next_page)

#url = 'https://www.imdb.com/title/tt0111161/reviews?ref_=ttexrv_ql_3'
#pythonResponse = requests.get(url)
#content = pythonResponse.text

titles = []
reviews = []
driver.get(next_page)

#content = driver.text
#soup = BeautifulSoup(driver,"lxml")

content = driver.page_source
soup = BeautifulSoup(content, "lxml")
t = random.randrange(7,10)
print(t)
for i in range(0, t):
  more_buttons = driver.find_element("id", 'load-more-trigger')
  if more_buttons[0].is_displayed():
      driver.execute_script("arguments[0].click();", more_buttons[0])
      time.sleep(5)

content = driver.page_source

soup = BeautifulSoup(content, "lxml")
title = soup.find_all('a', attrs={'class':'title'})
review = soup.find_all('div', attrs={'class':'text'})

for i in range(len(title)):
    titles.append(title[i].text)
for i in range(len(review)):
    reviews.append(review[i].text)

#print(soup) to print the xml code.

print(len(reviews), " reviews have been scraped.")
file_name = inp
df = pd.DataFrame({'Title':titles,'Reviews':reviews})
df.to_csv(inp+'_imdb_reviews.csv', index=False, encoding='utf-8')
