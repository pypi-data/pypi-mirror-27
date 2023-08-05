'''
This gets links to websites from PAS

You only get about 20 objects here as that is how many are per page.

Created on Aug 3, 2016

@author: maltaweel
'''

from bs4 import BeautifulSoup
import urllib2


#base url for database
url = 'https://finds.org.uk/database/search/results'


# Parse HTML of article, aka making soup
soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")

# Scrape for the links that have artefacts
links = soup.findAll('div',attrs={"typeof":"crm:E22_Man-Made_Object"})

#for look that prints out the links
for link in links:
    theLink=link["about"]  # this should be a link that is returned
    print theLink   # print it then just to see it's working
    
