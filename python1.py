#coding:utf-8

import urllib
import urllib2
import re
import json
import pymysql

class XIAMI:
	"""docstring for XIAMI"""
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#初始化headers
		self.headers  = { 'User-Agent' : self.user_agent }
		self.stories=[]
		self.enable = False
	
	def getPage(self,pageIndex):
		try:
			url = 'http://www.xiami.com/collect/ajax-get-list?_=1457785244323&id=151124730&limit=50&p='+str(pageIndex)
			request = urllib2.Request(url,headers = self.headers)
			response = urllib2.urlopen(request)
			pageContent = response.read().decode('utf-8')
			return pageContent
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"连接虾米音乐失败,原因:",e.reason
				return None


	def getPageItems(self,pageIndex):
		pageContent = self.getPage(pageIndex)
		if not pageContent:
			print "页面加载失败...."
			return None
		print pageContent

		ddata = json.loads(pageContent,'utf-8')
		pageCnt = ddata['result']['total_page']
		print pageCnt
		
		for item in ddata['result']['data']:
			self.stories.append([int(item['song_id']),int(item['artist_id']),item['name'],item['artist_name']])


		self.pageIndex = self.pageIndex + 1

		if self.pageIndex <= pageCnt :
		   self.getPageItems(self.pageIndex)
		

		

	def start(self):
		print "开始读取虾米音乐"
		self.pageIndex=1;
		self.getPageItems(self.pageIndex)

		





			# try:
			# 	with connection.cursor() as cursor:
			#         # Create a new record
			# 		sql = "INSERT INTO `songs` (`xiami_song_id`, `xiami_artist_id`,`name`,`artist_name`) VALUES (%s, %s, %s, %s)"
			#         cursor.execute(sql, (item['song_id'],item['artist_id'],item['name'],item['artist_name']))
			#     # connection is not autocommit by default. So you must commit to save
			#     # your changes.
			# finally:
			# 	print u"插入成功,歌曲:",item['name']

			#     # with connection.cursor() as cursor:
			#     #     # Read a single record
			#     #     sql = "SELECT `id`, `name` FROM `songs` WHERE `xiami_id`=%s"
			#     #     cursor.execute(sql, ('1770885848'))
			#     #     result = cursor.fetchone()
			#     #     print(result)

spider = XIAMI()
spider.start()

connection = pymysql.connect(host='yayayouji.com',
                             user='remote_oceancx',
                             password='Wf6796503.',
                             db='music',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print str(len(spider.stories))
for story in spider.stories:
	print story[0],story[1],story[2],story[3]
	try:
		with connection.cursor() as cursor:
			sql = "INSERT INTO `songs` (`xiami_song_id`, `xiami_artist_id`,`name`,`artist_name`) VALUES (%s, %s, %s, %s)"
			cursor.execute(sql, (story[0],story[1],story[2],story[3]))
			connection.commit()
	except Exception, e:
		raise e