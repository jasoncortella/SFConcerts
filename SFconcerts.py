import requests
from bs4 import BeautifulSoup

url = "http://www.foopee.com/punk/the-list/by-date.0.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
x = soup.find_all('a') 
indexList = []
for i, item in enumerate(x):
    if 'name="' in str(item):
        indexList.append(i)
flag = False
for i in range (indexList[0], indexList[1]):
    a = (2 if i == indexList[0] else 1) # if on a date field, selects date, otherwise selects venue / artist
    z = str(x[i]).split(">")[a].split("<")[0]
    if '<a name="' in str(x[i]):
        print(z)
    if '<a href="by-club' in str(x[i]):
        flag = True if "S.F." in z else False # only display the concerts in S.F. I'm not tryna go to San Jose cmon
        if flag:
            print("\t" + z)
    if '<a href="by-band' in str(x[i]):
        if flag:
            print("\t\t" + z)