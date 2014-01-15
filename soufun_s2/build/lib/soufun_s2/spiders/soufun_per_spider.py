# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from HTMLParser import HTMLParser
from soufun_s2.items import SoufunItem,ImageItem
from scrapy import log
from scrapy.http import Request
import urllib2,urllib,httplib
import urlparse
import MySQLdb
import sys
import re

class soufun_per_spider(CrawlSpider):
	name = "soufunper"
	allowed_domains = ["soufun.com"]
	start_urls = []
	rules = [
		Rule(SgmlLinkExtractor(allow=('/agent/agentnew/aloneesfhlist.aspx.*','/agent/agent/AloneHouseList.aspx','/Agent/AgentNew/AloneEsfHList.aspx.*')), follow=True),
		Rule(SgmlLinkExtractor(allow=('/chushou/.*','/shou/.*' )), callback='parse_item_house')
	]

	def __init__(self,my_setting, level=None, *args, **kwargs):
		super(soufun_per_spider, self).__init__(*args, **kwargs)
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		self.my_setting = my_setting

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		my_setting = {
					"host":settings.get("MYSQL_HOST"),
					"dbname":settings.get("MYSQL_DBNAME"),
					"user":settings.get("MYSQL_USER"),
					"passwd":settings.get("MYSQL_PASSWD")
					}		
		return cls(my_setting)

	def spider_closed(self, spider):

		if self.start_urls:
			try:
				conn=MySQLdb.connect(
					host=self.my_setting['host'],
					user=self.my_setting['user'],
					passwd=self.my_setting['passwd'],
					db=self.my_setting['dbname'],
					port=3306,charset='utf8'
					)
				cur=conn.cursor()
				cur.execute("update agent_store set is_finish = 1 where store_url=%s",self.start_urls)
				conn.commit()
				cur.close()
				conn.close()
				r=urllib.urlopen("http://agent.vsoufang.cn/custom/sendmsg?agent_open_id=%s",self.agent_open_id)					
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	def start_requests(self):
		result = self.getData()
		if result:
			request = Request(result[0], dont_filter=True)
			self.start_urls.append(result[0])
			self.agent_open_id = result[2]
			yield request
    
    # return the store_url,agent_open_id,check_status of data which is  waiting for synchroniz 
    # update the waiting status  to synchronizing status
	def getData(self):
		try:
			conn=MySQLdb.connect(
					host=self.my_setting['host'],
					user=self.my_setting['user'],
					passwd=self.my_setting['passwd'],
					db=self.my_setting['dbname'],
					port=3306,charset='utf8'
				)
			cur=conn.cursor()
			cur.execute('select store_url,check_status,agent_open_id from agent_store where is_finish = 0 order by check_status limit 0,1')
			result=cur.fetchone()
			if result:
				check_status = int(result[1])+1
				cur.execute("update agent_store set check_status =%s,update_count =0,insert_count=0,is_finish = 2 where store_url=%s",(check_status,result[0]))
				conn.commit()
			cur.close()
			conn.close()
			return result
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	def parse_item_house(self, response):
		item = SoufunItem()		
		item['house_id']     = self.getHouseId(response.url)
		item['title']       = self.getHouseTitle(response)
		item['agent_tel']   = self.getAgentTelephone(response)
		item['pic_list']    = self.getHousePicList(response)	
		item['description'] = self.getHouseDescription(response)
		item['dicts']       = self.getHouseDicks(response)
		item['url']         = response.url
		item['types']		= self.getHouseTpye(response.url)
		item['location']	= self.getHouseLocation(response)
		item['labels']      = self.getHouseLabels(response)
		item['store_url']   = self.start_urls[0]
		item['open_id']      = self.agent_open_id
 		return item

	def getAgentStore(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//dt[@id="esfshxq_201"]/a'
		results= hxs.xpath(xnode)
		agent_store = ''
		if results:
			agent_store = results[len(results)-1].xpath('@href').extract()[0].strip()
			print agent_store
		return agent_store	

	def getHouseTpye(self,url):
		pattern = re.compile(r'/(\w+).sh.soufun.com/')
		match = pattern.search(url)
		types = match.group(1)
		if match:
			types = match.group(1)
			if match.group(1) == 'esf':
				pattern = re.compile(r'http://esf.sh.soufun.com/chushou/(\d+)_')
				match = pattern.search(url)
				if match:
					if match.group(1) == '3':
						types =  'house'
					if match.group(1) == '10':
						types = 'villa'
		return types

	def getHouseId(self,url):
		pattern = re.compile(r'shou/(.*).htm')
		match = pattern.search(url)
		result = ''
		if match:
			result = match.group(1)
		return result

	def getHouseTitle(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//div[@class="title"]/h1'
		result= hxs.xpath(xnode).extract()
		title = ''
		if result:
			title = self.strip_tags(result[0].strip()).replace(' ','').replace('\r','').replace('\n','')
		return title

	def getAgentTelephone(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//span[@id="mobilecode"]/text()'
		result = hxs.xpath(xnode).extract()
		tel = ''
		if result:	
			tel = result[0].strip()
		return tel

	def getHousePicList(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//div[@class = "describe mt10"]//img[contains(@src,"jpg")]//@src'
		results = hxs.xpath(xnode)
		items = []
		for result in results:
			item = ImageItem()
			image_relative_url = result.extract()
			image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
			item['image_urls'] = [image_absolute_url]
			items.append(item)
		return items 

	def getHouseDescription(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//div[@class="describe mt10"]//span/text()'
		results = hxs.xpath(xnode).extract()
		description = ''
		if results:
			description = results
		else:
			xnode = '//div[@class="describe mt10"][1]/div/text()'
			results = hxs.xpath(xnode).extract()
			if results:
				description = results
		return ''.join(description)

	def getHouseLabels(self,response):
		hxs = HtmlXPathSelector(response)
		results = hxs.xpath('//p[@class = "note"]/span')
		labels = ''	
		for result in results:
			l = result.xpath('text()').extract()
			if l:
				labels = labels+l[0].strip()+' '
		return  labels	

	def getHouseTotalPrice(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//dt[@class="gray6 zongjia1"]/span[2]/text()'
		result= hxs.xpath(xnode).extract()
		totalprice = ''
		if result:
			totalprice = result[0].strip()
		return totalprice

	def getHouseDicks(self,response):
		dicts ={}
		hxs = HtmlXPathSelector(response)
		xnode1 = '//div[@class="info"]//dt'
		results1= hxs.xpath(xnode1)
		xnode2 = '//div[@class="info"]//dd'
		results2= hxs.xpath(xnode2)
		results = results1+results2

		for result in results:
			content =  self.strip_tags(result.extract()).replace(' ','').replace('\r','').replace('\n','')
			array = content.split(u"：")
			if len(array)>1:
				dicts[array[0]] = array[1]
		return dicts

	def getHouseLocation(self,response):
		hxs = HtmlXPathSelector(response)
		result= hxs.xpath('//div[@class="traffic mt10"]/p[1]/text()').extract()
		location = 'location is empty'

		if result:
			location = result[1].strip()		
		return location		

	def strip_tags(self,html):
		s = MLStripper()
		s.feed(html)
		return s.get_data()

	def __str__(self):
		return "ProductSpider"		

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)





