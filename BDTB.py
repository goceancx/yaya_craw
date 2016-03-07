# coding:utf-8
import urllib2
import re
# import Tool

#处理页面标签类
class Tool:
	#去除img标签,7位长空格
	removeImg = re.compile('<img.*?>| {7}|')
	#删除超链接标签
	removeAddr = re.compile('<a.*?>|</a>')
	#把换行的标签换为\n
	replaceLine= re.compile('<tr>|<div>|</div>|</p>')
	#把表格制表td替换为\t
	replaceTD = re.compile('<td>')
	#把段落开头替换为\n加空两格
	replacePara = re.compile('<p.*?>')
	#将换行符或双换行符替换为\n 
	replaceBR = re.compile('<br><br>|<br>')
	#将剩余标签剔除
	removeExtraTag = re.compile('<.*?>')
	def replace(self , x):
		x = re.sub(self.removeImg,"",x)
		x = re.sub(self.removeAddr,"",x)
		x = re.sub(self.replaceLine,"\n",x)
		x = re.sub(self.replaceTD,"\t",x)
		x = re.sub(self.replacePara,"\n    ",x)
		x = re.sub(self.replaceBR,"\n",x)
		x = re.sub(self.removeExtraTag,"",x)
		return x.strip()

#百度贴吧爬虫类
class BDTB:

	#初始化,传入基地址,是否只看楼主的参数
	def __init__(self, baseUrl,seeLZ,floorTag):
		self.baseURL = baseUrl
		self.user_agent= 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = {'User-Agent' : self.user_agent}
		self.seeLZ ='?see_lz='+str(seeLZ)
		self.tool =Tool()
		self.file = None
		self.floor = 1
		self.defaultTitle= u"百度贴吧"
		self.floorTag = floorTag


	#传入页码,获取该页帖子的代码
	def getPage(self,pageNum):
		try:
			url = self.baseURL + self.seeLZ +'&pn=' + str(pageNum)
			request = urllib2.Request(url,headers = self.headers)
			response =urllib2.urlopen(request)
			# print response.read().decode('utf-8')
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print u"连接百度贴吧失败,错误原因",e.reason
				return None

	def getTitle(self,page):
		pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow.*?">(.*?)</h3>',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None


	def getPageNum(self,page):
		pattern = re.compile('<li class="l_reply_num.*?class="red">(.*?)</span>.</li>',re.S)
		result = re.search(pattern,page)		
		if result:
			return result.group(1).strip()
		else:
			return None


	def getContent(self,page):
		pattern = re.compile('<div id="post_content_.*?">(.*?)</div>',re.S)
		items = re.findall(pattern,page)
		contents=[]
		for item in items:
			content ="\n" + self.tool.replace(item) + "\n"
			contents.append(content.encode('utf-8'))
		return contents

	def setFileTitle(self,title):
		if title is not None:
			self.file = open(title +".txt", "w+")
		else:
			self.file = open(self.defaultTitle +".txt","w+")

	def writeData(self,contents):
		for item in contents:
			if self.floorTag == '1':
				floorLine = "\n" + str(self.floor) + u"-----------------------------------------------------------------------------------------\n"
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print "URL已失效,请重试"
			return
		try:
			print "该帖子共有" + str(pageNum) +"页"
			for i in range(1,int(pageNum)+1):
				print "正在写入第" + str(i) + "页数据"
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError, e:
			print "写入异常,原因" + e.message
		finally:
			print "写入任务完成"


print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL,seeLZ,floorTag)
bdtb.start()

