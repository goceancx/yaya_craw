# coding:utf-8

from bs4 import BeautifulSoup
import urllib2
import re

#http://www.xiami.com/artist/61594
# '莫文蔚', 2017
# 'Stefanie Heinzmann', 56874
# '江语晨', 56106
# '郁可唯', 63802
# 'Ramzi', 61594
# 'Nelly', 24974
# 'Jo De La Rosa', 44343
# 'Bonobo', 52220
# 'Ne-Yo', 34779
# 'Sarah Harmer', 28349
# 'Bruno Mars', 74124
# 'Shayne Ward', 23463
# 'Avant', 34922
# 'Ke$ha', 66804
# 'Tonya Mitchell', 56808
# 'The Wanted', 77535
# 'Elliott Yamin', 23604
# 'Deep Side', 63172
# 'George Nozuka', 23988
# 'Stevie Hoang', 23986
# 'Flipsyde', 62035
# 'R.Kelly', 11641
# 'Apink', 87417
# 'Ina', 83094
# 'Trey Songz', 44521

artistIds= ['2017','56874','56106','63802','61594','24974','44343','52220','34779','28349','74124','23463','34922','66804','56808','77535','23604','63172','23988','23986','62035','11641','87417','83094','44521']
airtests= ['莫文蔚','Stefanie Heinzmann','江语晨','郁可唯','Ramzi','Nelly','Jo De La Rosa','Bonobo','Ne-Yo','Sarah Harmer','Bruno Mars','Shayne Ward','Avant','Ke$ha','Tonya Mitchell','The Wanted','Elliott Yamin','Deep Side','George Nozuka','Stevie Hoang','Flipsyde','R.Kelly','Apink','Ina','Trey Songz']

index = 0
for aid in artistIds:

	url ='http://www.xiami.com/artist/'+aid
	# url ='http://www.xiami.com/artist/'+'2017'
	request = urllib2.Request(url)
	request.add_header("User-Agent" , "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)")
	response =urllib2.urlopen(request)
	#print response
	cont = response.read().decode('utf-8')
	#print  cont

	soup = BeautifulSoup(cont , 'html.parser',from_encoding='utf-8')


	tables=  soup.find_all('table' ,class_='track_list')

	print airtests[index]

	for t in tables:
		for tr in t.tbody.children:
			try:
				print tr.contents[5].a['href'].encode('utf-8') , tr.contents[5].a.string.encode('utf-8')
			except Exception, e:
				pass

	index=index+1
