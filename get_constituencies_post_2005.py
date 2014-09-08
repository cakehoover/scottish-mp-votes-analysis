'''
Get constituencies post the 2005 general election, from Mapit.
Correctly generates a list of 59 constituencies.
'''
import csv
import json
import requests
from operator import itemgetter
from pyquery import PyQuery as pq

url_post_2005 = 'http://mapit.mysociety.org/areas/WMC'
response = requests.get(url_post_2005)
data = json.loads(response.text)

output = csv.writer(open('./data/scottish_constituencies_post_2005.csv', 'w'))
output.writerow(['Constituency'])

constituencies = []

for k in data:
    c = data[k]
    if c['country_name'] == 'Scotland':
        constituencies.append(c['name'])

constituencies = sorted(constituencies)
for c in constituencies:
    output.writerow([c])
