#  coding:utf-8 
__author__='CQC'
import urllib2
import re
import thread
import time

#糗事百科爬虫类
class QSBK:

	#初始化方法,定义一些变量
	def __init__(self):
		self.pageIndex=1
		self.user_agent= 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		#初始化headers
		self.headers = {'User-Agent' : self.user_agent}
		self.stories =[]
		self.enable =False


	#传入某一页的索引获得页面代码
	def getPage(self,pageIndex):
		try:
			url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
			request =urllib2.Request(url,headers = self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"连接糗事百科失败,错误原因",e.reason
				return None

	#传入某一页代码,返回本页不带图片的段子列表
	def getPageItems(self,pageIndex):
		pageCode = self.getPage(pageIndex)
		if not pageCode:
			print "页面加载失败...."
			return None
		pattern = re.compile('<div.*?author clearfix">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
'content">(.*?)<!--.*?-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)

		items = re.findall(pattern,pageCode)
		pageStories = []
		for item in items:
			hasImg= re.search("img",item[2])
			if not hasImg:
				replaceBR  = re.compile('<br/>')
				text = re.sub(replaceBR,"\n",item[1])
				pageStories.append([item[0].strip(), text.strip() ,item[3].strip()])
		return pageStories


	#加载并提取页面内容,加入到列表中
	def loadPage(self):
		#如果当前未看的页数少于2页,则加载新一页
		if self.enable == True:
			if len(self.stories) < 2:
				#获取新一页
				pageStories = self.getPageItems(self.pageIndex)
				if pageStories:
					self.stories.append(pageStories)
					self.pageIndex +=1

	def getOneStory(self,pageStories,page):
		#遍历一页的段子
		for story in pageStories:
			input = raw_input()
			self.loadPage()
			if input == "Q":
				self.enable = False
				return
			print u"第%d页\t发布人:%s\t赞:%s\n%s" %(page,story[0],story[2],story[1])

	#开始方法
	def start(self):
		print u"正在读取糗事百科,按回车查看新段子,Q退出"
		#使变量为True
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories) > 0 :
				pageStories = self.stories[0]
				nowPage+= 1
				del	self.stories[0]
				self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()				





