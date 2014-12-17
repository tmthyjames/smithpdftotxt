#!/usr/bin/env python

# grabs all links containing PDFs and converts them to txt files

import subprocess
import re
import requests
from bs4 import BeautifulSoup
from pattern.web import URL
import logging
import os


url = 'http://www.txlottery.org/export/sites/lottery/Media/News_Releases'
req = requests.get(url)
soup = BeautifulSoup(req.content)
sidenav = soup.find_all('ul',{'class':'side-nav'})

releases = []
for s in sidenav:
    for link in s('a'):
        base = 'http://www.txlottery.org'
        link = base+link.get('href')
        releases.append(link)

links = []
for link in releases:
    url = link
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    gdata = soup.find_all('div',{'class':'row'})
    for g in gdata:
        baselink = 'http://www.txlottery.org'
        try:
            if re.findall('[0-9]{2} [A-Za-z]{3} [0-9]{2}',str(g)):
                date = re.findall('[0-9]{2} [A-Za-z]{3} [0-9]{2}',str(g))
        except:
            pass
        for link in g('a'):
            try:
                if re.search('pdf$',str(link.get('href')),flags=re.IGNORECASE):
                    link = baselink+link.get('href')
                    pdfurl = URL(link)
                    pdfext = '/Users/macuser/Desktop/smithpdf'+link[link.rfind('/'):]
                    pdfext = re.sub('[!@#\$%\^&*]','',str(pdfext))
                    f = open(pdfext, 'wb')
                    f.write(pdfurl.download(cached=False))
                    f.close()
                    links.append(link)
                    callThis = 'pdftotext '+pdfext+' '+'/Users/macuser/Desktop/smithtxt'+pdfext[pdfext.rfind('/'):-4]+'.txt'
                    subprocess.call(callThis,shell=True)
            except:
                logging.exception('')
                pass


patht = '/Users/macuser/Desktop/smithtxt'
pathp = '/Users/macuser/Desktop/smithpdf'
smithtxt = os.listdir(patht)
smithpdf = os.listdir(pathp)
smithtxt = smithtxt[1:]
smithpdf = smithpdf[1:]
newsmithtxt = [s[:-4] for s in smithtxt]
newsmithpdf = [s[:-4] for s in smithpdf]


dates = []
text = []
regex = re.compile('[a-zA-Z]{3,}\.? ?[0-9]{1,2},? [0-9]{2,4}|[0-9]{2} [a-zA-Z]{3,}, [0-9]{4}')
for txt in smithtxt:
    file = os.path.join(patht,txt)
    content = open(file).read()
#     for line in content:
    try:
        if re.search(regex,str(content)):
            match = re.findall(regex, str(content))[0]
            dates.append(match)
            text.append(txt)
    except:
        pass


print 'number of items in dates: ', len(dates)
print 'number of items in text: ', len(text)

print 'missing items: ', (set(smithtxt) - set(text))

# create dict to map dates to titles
dictionary = dict(zip(dates, text))

# write dict to csv
with open('/Users/macuser/Desktop/dates&titles.csv', 'w') as f:
    [f.write('{0},{1}\n'.format(key, value)) for key, value in dictionary.items()]














