import requests
from bs4 import BeautifulSoup as bs
import sqlite3

url = "https://ibighit.com/txt/jpn/profile/"
header = {"User-Agent" : "Mozilla/5.0"}
soup = bs(requests.get(url, headers=header).content, 'html.parser')

name = []
birth = []
height = []
weight = []

profile_soup = bs(requests.get(url, headers=header).content, 'html.parser') # get the sourcce cord
for dl in profile_soup.find_all('dl'):
  for dt in dl.find_all('dt'):
    name.append(dt.text)
  for ul in dl.find_all('ul'):
    lis = []
    for i in range(3):
      lis.append(ul.find_all('li')[i])
    print(lis)
    cnt = 0
    for l in lis:
      l = str(l).split(':')
      a = l[1].split('<')
      if cnt == 0: birth.append(a[0].strip())
      if cnt == 1: height.append(a[0].strip())
      if cnt == 2: 
        weight.append(a[0].strip().replace('\u200b', ''))
      cnt += 1

con = sqlite3.connect('txt.db')
cur = con.cursor()
cur.executescript("""
drop table if exists member_data;
CREATE TABLE member_data(name, birth, height, weight)
""")

for x, y, z, w in zip(name, birth, height, weight):
  cur.execute("INSERT INTO member_data VALUES(?,?,?,?);", (x, y, z, w))

con.commit()
# print(name, birth, height, weight)