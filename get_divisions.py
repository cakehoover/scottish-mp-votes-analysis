'''
Scrape the full list of Commons divisions since 1997 from Public Whip.
Output division names and URLs to a CSV file.
'''
import csv
import requests
from pyquery import PyQuery as pq

PW_URL = 'http://www.publicwhip.org.uk/'

fieldnames = ['parliament', 'date', 'name', 'url']
output = csv.DictWriter(open('./data/commons_divisions_since_1997.csv', 'w'),
                        fieldnames=fieldnames)
output.writeheader()

for year in [2010, 2005, 2001, 1997]:
    url = '%s%s%s' % (PW_URL, 'divisions.php?rdisplay=', year)
    response = requests.get(url)
    doc = pq(response.content)
    divisions = doc('table.votes tr:not(.headings)')
    for division in divisions:
        d = pq(division)
        house = d('td:first').text().strip().lower()
        if house == 'commons':
            entry = {}
            subject = d('td:eq(3)')
            entry['parliament'] = year
            entry['date'] = d('td:eq(1)').text().encode('utf-8')
            entry['name'] = subject.text().encode('utf-8')
            entry['url'] = '%s%s&display=allvotes' % (PW_URL, subject('a').attr('href').encode('utf-8'))
            output.writerow(entry)
