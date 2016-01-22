# coding:utf-8
from bs4 import BeautifulSoup
import urllib2
import re


url ='http://www.xiami.com/artist/2017'

request = urllib2.Request(url)
request.add_header("User-Agent" , "Mozilla/5.0")
response =urllib2.urlopen(request)
#print response
cont = response.read()
print  cont

soup = BeautifulSoup(cont , 'html.parser',from_encoding='utf-8')

link_node = soup.find_all('a', href=re.compile(r"/song/\d+$"))
for link in link_node:
	print link.name  , link['href'] , link.get_text()

