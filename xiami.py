# coding=utf-8

import urllib2
import re

def httpGet(uid,pageNum):
	try:
		user_agent= 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#初始化headers
		headers = {'User-Agent' : user_agent}
		url = 'http://www.xiami.com/space/lib-song/u/' + str(uid)+'/page/'+ str(pageNum)
		request =urllib2.Request(url,headers= headers)
		response = urllib2.urlopen(request)
		pageCode = response.read().decode('utf-8')
		return pageCode
	except urllib2.URLError, e:
		if hasattr(e,"reason"):
			print u"网络连接失败,错误原因:",e.reason
			return None 	


def getPageItems(pageNum):
		pageCode=httpGet('49435626',pageNum)
		if not pageCode:
			print "页面加载失败...."
			return None
		pattern = re.compile('<tr class=".*?" id="lib_song_(.*?)" title=".*?">.*?<td class="song_name">.*?<a.*?>(.*?)</a>',re.S)

		items = re.findall(pattern,pageCode)
		pageStories = []
		for item in items:
			pageStories.append([item[0],item[1]])
			print unicode(item[0]) , unicode(item[1])
		return pageStories

# content= httpGet("49435626")
for i in range(1,11):
	getPageItems(i)

#http://www.xiami.com/space/lib-song/u/49435626