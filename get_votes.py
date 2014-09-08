'''
For all Commons divisions since 1997, do the following:
- Count the number of ayes and noes.
- Count up the number of ayes and noes without Scottish MPs.
- Compare the two results to see if they are different.
The names of Scottish constituencies changed in 2005, so make
sure we use the appropriate list.
'''
import csv
import requests
import sys
from pyquery import PyQuery as pq

# Load in the Scottish constituencies before + after the 2005 election.
reader = csv.DictReader(open('./data/scottish_constituencies_pre_2005.csv'))
scottish_constituencies_pre_2005 = []
for row in reader:
    scottish_constituencies_pre_2005.append(row['Constituency'])
reader = csv.DictReader(open('./data/scottish_constituencies_post_2005.csv'))
scottish_constituencies_post_2005 = []
for row in reader:
    scottish_constituencies_post_2005.append(row['Constituency'])

# Create a place to keep the results.
fieldnames = ['parliament', 'date', 'name', 'url', 'ayes', 'noes',
              'ayes_noscotland', 'noes_noscotland', 'different']
output = csv.DictWriter(open('./data/commons_divisions_with_results.csv',
                             'w'), fieldnames=fieldnames)
output.writeheader()

# Load in the Commons divisions.
reader = csv.DictReader(open('./data/commons_divisions_since_1997.csv'))
for row in reader:
    print row['date'], row['name']
    # if row['url'] != 'http://www.publicwhip.org.uk/division.php?date=2003-07-08&number=280&display=allvotes':
    #     continue

    # Use the right list of Scottish constituencies.
    scot_constituencies = []
    if row['parliament'] == '1997' or row['parliament'] == '2001':
        scot_constituencies = scottish_constituencies_pre_2005
    else:
        scot_constituencies = scottish_constituencies_post_2005

    # Keep score of the results.
    row['ayes'] = 0
    row['noes'] = 0
    row['ayes_noscotland'] = 0
    row['noes_noscotland'] = 0

    # Scrape votes.
    response = requests.get(row['url'])
    doc = pq(response.content)
    votes = doc('table.votes tr:not(.headings)')
    vote_name = doc('h1').text()
    for vote in votes:
        doc = pq(vote)
        constituency = doc('td:eq(1)').text()
        value = doc('td:eq(3)').text().strip()

        # Count up the ayes and noes (including the tellers' votes).
        if value == 'aye' or value == 'tellaye':
            row['ayes'] += 1
            if constituency not in scot_constituencies:
                row['ayes_noscotland'] += 1
        elif value == 'no' or value == 'tellno':
            row['noes'] += 1
            if constituency not in scot_constituencies:
                row['noes_noscotland'] += 1
        elif value == 'both':
            row['ayes'] += 1
            row['noes'] += 1
            if constituency not in scot_constituencies:
                row['ayes_noscotland'] += 1
                row['noes_noscotland'] += 1
        else:
            print 'Unknown vote type:', value

    # Check whether no Scottish votes would have changed the result.
    carried_by_ayes = (row['ayes'] > row['noes'])
    carried_by_ayes_noscotland = (row['ayes_noscotland'] > row['noes_noscotland'])
    row['different'] = (carried_by_ayes != carried_by_ayes_noscotland)
    if row['different']:
        print vote_name
        print '!!!!!!!! DIFFERENT RESULTS!!!!!!!'
        carried = 'Ayes' if carried_by_ayes else 'Noes'
        carried_noscotland = 'Ayes' if carried_by_ayes_noscotland else 'Noes'
        print 'Actual results: Carried by %s: %s ayes to %s noes' % (carried, row['ayes'], row['noes'])
        print 'Without Scotland: Carried by %s: %s ayes to %s noes\n' % (carried_noscotland, row['ayes_noscotland'], row['noes_noscotland'])

    output.writerow(row)
