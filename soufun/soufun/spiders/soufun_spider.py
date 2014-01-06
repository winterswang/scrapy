# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from HTMLParser import HTMLParser
from soufun.items import SoufunItem,ImageItem
from scrapy import log
import urlparse
import sys
import re
class soufun2_spider(CrawlSpider):
	name = "soufun2"
	allowed_domains = ["sh.soufun.com"]
	start_urls = ["http://esf.sh.soufun.com/agenthome/-i31-j310/"]
	rules = [
		Rule(SgmlLinkExtractor(allow=('/a/.*','/agenthome.*-j310/$','/agent/agentnew/aloneesfhlist.aspx.*','/Agent/AgentNew/AloneEsfHList.aspx.*')), follow=True),
		Rule(SgmlLinkExtractor(allow=('esf.sh.soufun.com/chushou/.*','esf.sh.soufun.com/shou/.*' )), callback='parse_item_house')
	]

	def parse_item_house(self, response):
		item = SoufunItem()		
		item['houseid']     = self.getHouseId(response.url)
		item['title']       = self.getHouseTitle(response)
		item['agent_tel']   = self.getAgentTelephone(response)
		item['pic_list']    = self.getHousePicList(response)	
		item['description'] = self.getHouseDescription(response)
		item['dicts']       = self.getHouseDicks(response)
		item['url']         = response.url
		item['types']		= self.getHouseTpye(response.url)
		item['location']	= self.getHouseLocation(response)
		item['labels']      = self.getHouseLabels(response)
		item['store_url']   = self.getAgentStore(response)		
		return item
		print response.url

	def getAgentStore(self,response):
		hxs = HtmlXPathSelector(response)
		xnode = '//dt[@id="esfshxq_201"]/a/@href'
		result= hxs.xpath(xnode).extract()
		agent_store = ''
		if result:
			agent_store = result[0].strip()
		return agent_store	

	def getHouseTpye(self,url):
		pattern = re.compile(r'/(\w+).sh.soufun.com/(\d+)_')
		match = pattern.search(url)
		types = ''
		if match:
			types =  match.group(1)
			if types == 'esf' and match.group(2) == 10:
				return 'house'
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
		L = []
		for result in results:
			# item = ImageItem()
			image_relative_url = result.extract()
	        # image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
	        # item['image_urls'] = [image_absolute_url]
	        L.append(image_relative_url)
		return L 

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

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)





