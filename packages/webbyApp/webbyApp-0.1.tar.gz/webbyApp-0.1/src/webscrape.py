'''
This simply gets some data from a record within PAS.

The data recovered are the object, image, and description

Created on Jul 27, 2016

@author: maltaweel
'''
from bs4 import BeautifulSoup
import time
import urllib2


# The base url for the example
url = 'https://finds.org.uk/database/artefacts/record/id/662834'

#current time stamp to be used in naming the jpg file created
timestamp = time.asctime() 

# Parse HTML of article, aka making soup
soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")

# Scrape article main img
links = soup.findAll('img')
for link in links:
    
    #get the current time
    timestamp = time.asctime() 
    
    #get the link that is in src (i.e., an image from html)
    link = link["src"]
    if "https://finds.org.uk/images/" not in link:  #the link without finds.org are skipped
        continue
    if "thumbnails" in link:   #we don't want thumbnails, so skip those
        continue
    
    #print the link (i.e., shold be the correct image link)
    print(link)   
    
    #now get the data using the urllib2 library 
    download_img = urllib2.urlopen(link)
    
    #create the image stream (should go to your current folder this module is in)
    txt = open('%s.jpg' % timestamp, "wb")
    
    #write the binary data
    txt.write(download_img.read())

    #close the image file
    txt.close()

#get the main topic, which should be the object in this link
obj= soup.find('h1').getText()
print (obj)

#now get the pas description about the object
text=soup.find("div",attrs={"property":"pas:description"})

#get rid of the html tags and just get the one between <p>
finalText=text.find('p').getText()

#print the final result
print(finalText)