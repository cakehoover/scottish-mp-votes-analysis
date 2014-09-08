'''
Get constituencies before the 2005 general election, from Wikipedia.
Correctly generates a list of 72 constituencies.
We also need to add two constituencies that changed name in 2005:
PublicWhip uses the newer name for these constituencies.
'''
import csv
import requests
from pyquery import PyQuery as pq

url_pre_2005 = 'http://en.wikipedia.org/wiki/Scottish_Westminster_constituencies_1997_to_2005'
response = requests.get(url_pre_2005)
doc = pq(response.content)
rows = doc('table.wikitable:first tr')
constituencies = []
for row in rows:
    d = pq(row)
    constituency = d('td:not([rowspan]):first').text()
    if constituency:
        constituency = constituency.replace('BC', '').replace('CC', '').strip()
        constituencies.append(constituency)

rows = doc('table.wikitable:last tr')
for row in rows:
    d = pq(row)
    d = d('td:eq(1)')
    if d.text():
        constituency = d('td').text().strip()
        if constituency:
            constituencies.append(constituency)

output = csv.writer(open('./data/scottish_constituencies_pre_2005.csv', 'w'))
output.writerow(['Constituency'])
constituencies = sorted(constituencies)
for c in constituencies:
    output.writerow([c])

output.writerow(['Na h-Eileanan an Iar'])  # formerly Western Isles
output.writerow(['East Renfrewshire'])  # formerly Eastwood
