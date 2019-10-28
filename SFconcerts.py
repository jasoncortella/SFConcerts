import requests
from bs4 import BeautifulSoup
from datetime import datetime

#SETTINGS ------------------------------------------------------------------------------------------------------------------------

daysToDisplay = 10  # Select the number of days of concerts to display.
                   # Currently, can only display through next Sunday, such that the max is 8-14 depending on day of the week

cities = []        # Select cities to display. Comment out undesired cities
                   # Note - Only cities near S.F. included. See http://www.foopee.com/punk/the-list/ for full list of cities
#cities.append('Alameda')
#cities.append('Berkeley')
cities.append('Oakland')
cities.append('S.F.')
#cities.append('San Jose')
#cities.append('Saratoga')

#SETTINGS ------------------------------------------------------------------------------------------------------------------------


day = datetime.now().weekday()
start = 0 if day != 0 else 1 # If the script is ran on a monday, the second page must be used due to the site's update frequency

url1 = "http://www.foopee.com/punk/the-list/by-date.{}.html".format(start) # current week
page1 = requests.get(url1)
soup1 = BeautifulSoup(page1.text, 'html.parser')
indexList1 = []
response1 = soup1.find_all('a')
for i, item in enumerate(response1): # Find date separators
    if 'name="' in str(item):
        indexList1.append(i)
indexList1.append(len(response1)) # Set endpoint

if (daysToDisplay > (7 - day)): # Skip second GET request if not required
    url2 = "http://www.foopee.com/punk/the-list/by-date.{}.html".format(start + 1) # next week
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text, 'html.parser')
    response2 = soup2.find_all('a')
    indexList2 = []
    for i, item in enumerate(response2):
        if 'name="' in str(item):
            indexList2.append(i)
    indexList2.append(len(response2))

printed = 0
Flag = False
for j in range(7 - day): # Displays remaining concerts for the week
    if printed >= daysToDisplay:
        break
    for i in range (indexList1[j], indexList1[j+1]):
        field = (2 if i == indexList1[j] else 1) # if on field date field, selects date, otherwise selects venue / artist
        text = str(response1[i]).split(">")[field].split("<")[0]
        if '<field name="' in str(response1[i]):
            print(text)
        if '<a href="by-club' in str(response1[i]):
            Flag = True if any([city in text for city in cities]) else False # only display the concerts in selected cities
            if Flag:
                print("\t" + text)
        if '<a href="by-band' in str(response1[i]):
            if Flag:
                print("\t\t" + text)
    printed += 1
Flag = False
for j in range(7):
    if printed >= daysToDisplay:
        break
    for i in range (indexList2[j], indexList2[j+1]):
        field = (2 if i == indexList2[j] else 1) # if on field date field, selects date, otherwise selects venue / artist
        text = str(response2[i]).split(">")[field].split("<")[0]
        if '<a name="' in str(response2[i]):
            print(text)
        if '<a href="by-club' in str(response2[i]):
            Flag = True if any([city in text for city in cities]) else False # only display the concerts in selected cities
            if Flag:
                print("\t" + text)
        if '<a href="by-band' in str(response2[i]):
            if Flag:
                print("\t\t" + text)
    printed += 1