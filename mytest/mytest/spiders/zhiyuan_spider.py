# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from mytest.items import SoufunItem,HouseItem
from scrapy import log
import sys
import re

class zhiyuanSpider(CrawlSpider):
	name = "zhiyuan"
	allowed_domains = ["soufun.com"]
	start_urls = ["http://esf.sh.soufun.com/agenthome/-c5%d6%be%d4%b6%b5%d8%b2%fa-i31-j310/"]
	# start_urls = ['http://esf.sh.soufun.com/chushou/10_84622584.htm']
	rules = [
		Rule(SgmlLinkExtractor(allow=('/agenthome/-c5%d6%be%d4%b6%b5%d8%b2%fa.*-j310/$','/agent/agentnew/aloneesfhlist.aspx?&managername=.*','/agent/agentnew/aloneesfhlist.aspx?agentid=(\d+)&projname=&comarea=&pricemin=&pricemax=&purpose=&roomtype=&htype=&moretype=&page=.*')), follow=True),
		Rule(SgmlLinkExtractor(allow=('/a/.*')) , callback='parse_item_store', follow=True),
		Rule(SgmlLinkExtractor(allow=('esf.sh.soufun.com/chushou/.*', ),deny=('esf.sh.soufun.com/chushou/9_.*','office.sh.soufun.com/.*')), callback='parse_item_house_new')
		]
	def parse_item_store(self, response):
		#analysis store data: name,tel,store_url,company,head_url,store_name,circle
		reload(sys)
		sys.setdefaultencoding('utf-8')
		hxs = HtmlXPathSelector(response)
		name = hxs.xpath('//div[@class="rzname floatl"]/text()').extract()
		if name:
			print name[0]
		else:
			name = hxs.xpath('//div[@class="rzren"]/dl/dt/text()').extract()
			if name:
				print name[0]

		tel = hxs.xpath('//span[@class="phonenum"]/text()').extract()
		if tel:
			print tel[0]
		else:
			print "tel is empty\r\n"

		company = hxs.xpath('//ul[@class="cont02 mb10"]/li[1]/text()').extract()
		if len(company)>1:
			print company[1]
		else:
			company = hxs.xpath('//div[@class="rzxxL"]/dl/dd[1]/text()').extract()
			if company:
				print company[0]
			else:
				print "company is empty\r\n"

		store_name =  hxs.xpath('//ul[@class="cont03"]/li[2]/text()').extract()
		if store_name:
			print store_name[0]
		else:
			print "store_name is empty\r\n"

		head_url = hxs.xpath('//div[@class="rzren"]/img/@src').extract()
		if head_url:
			print head_url[0]
		else:
			head_url = hxs.xpath('//div[@class="photo"]/a/img/@src').extract()
			if head_url:
				print head_url[0]
			else:
				print "head_url is empty\r\n"
		dom = hxs.xpath('//ul[@class="cont02 mb10"]/li')
		for d in dom:			
			body = str(d.extract()).encode('utf-8')
			pattern = re.compile(ur'服务商圈：(\w+([,]?\w+){1,})', re.U)
			result = pattern.search(unicode(body))
			if result:
				print result.group(1)
		# circle = hxs.xpath('//ul[@class="cont02 mb10"]/li[3]/text()').extract()
		# if len(dom) ==6:
		# 	circle = hxs.xpath('//ul[@class="cont02 mb10"]/li[4]/text()').extract()
		# if circle:
		# 	print circle[0]
		# else:
		# 	circle = hxs.xpath('//div[@class="rzxxL"]/dl/dd[3]/text()').extract()
		# 	if circle:
		# 		print circle[0]
		# 	else:
		# 		print "circle is empty\r\n"	

		print response.url
	# def parse_item_store_new(self,response):

	def getHouseTpye(self,url):
		""" if shop return 2 if apartment return 0 if house return 1 it is used for different pattern to analysis data from website"""
		pattern = re.compile(r'/(\w+).sh.soufun.com/')
		print url
		match = pattern.search(url)
		if match and match.group(1) == 'shop':
			return 2 
		if match and match.group(1) == 'esf':
			pattern = re.compile(r'/chushou/(\d+).*htm')
			match = pattern.search(url)
			if match and match.group(1) == '3':
				return  0
			if match and match.group(1) == '10':
				return 1
	def parse_item_house_new(self,response):
		category = self.getHouseTpye(response.url)
		print category
		item = HouseItem()
		item['houseid']     = self.getHouseId(response.url)
		item['title']       = self.getHouseTitle(response,category)
		item['allprice']    = self.getHouseAllPrice(response,category)
		item['square']      = self.getHouseSquare(response,category)
		item['layout']      = self.getHouseLayout(response,category)
		item['age']         = self.getHouseAge(response,category)
		item['orientation'] = self.getHouseOrientation(response,category)
		item['floor']       = self.getHouseFloor(response,category)
		item['decoration']  = self.getHouseDecoration(response,category)
		item['labels']      = self.getHouseLabels(response,category)
		item['district']    = self.getHouseDistrict(response,category)
		item['location']    = self.getHouseLocation(response,category)
		item['huxing_pic']  = self.getHouseHuxingPic(response,category)
		item['pic_list']    = self.getHousePicList(response,category)
		item['agent_tel']   = self.getAgentTelephone(response,category)
		# return item

	def getHouseId(self,url):
		pattern = re.compile(r'shou/(.*).htm')
		match = pattern.search(url)
		result = ''
		if match:
			print match.group(1)
			result = match.group(1)
		return result
	def getHouseTitle(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("title",category)
		result= hxs.xpath(xnode).extract()
		title = ''
		if result:
			title = result[0].strip()
		else:
			print 'title is empty'
		print title
		return title	
	def getHouseAllPrice(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("allprice",category)
		result= hxs.xpath(xnode).extract()
		allprice = ''
		if result:
			allprice = result[0].strip()
		else:
			print 'allprice is empty'
		print allprice
		return allprice
	def getHouseSquare(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("square",category)
		result = hxs.xpath(xnode).extract()
		square = ''
		if result:
			square = result[0].strip()
		else:
			print 'square is empty'
		print square
		return square
	def getHouseLayout(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("layout",category)
		result = hxs.xpath(xnode).extract()
		layout = ''
		if result:
			layout = result[0].strip()
		else:
			print 'layout is empty'
		print layout
		return layout
	def getHouseAge(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("age",category)
		result = hxs.xpath(xnode).extract()
		age = ''
		if len(result)>1:
			age = result[1].strip()
		else:
			age = result[0].strip()
		if age :
			print age
		else:
			print 'age is empty'
		return age
	def getHouseOrientation(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("orientation",category)
		result = hxs.xpath(xnode).extract()
		orientation = ''
		if result:
			orientation = result[0].strip()
		else:
			print 'orientation is empty'
		print orientation
		return orientation							
	def getHouseFloor(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("floor",category)
		result = hxs.xpath(xnode).extract()
		floor = ''
		if len(result)>1:
			floor = result[1].strip()
		else:
			if result:
				floor = result[0].strip()
		if floor:
			print floor
		else:
			print 'floor is empty'
		return floor
	def getHouseDecoration(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("decoration",category)
		result = hxs.xpath(xnode).extract()
		decoration = ''
		if len(result)>1 :
			decoration = result[1].strip()
		elif result:
			decoration = result[0].strip()
		if decoration:
			print decoration
		else:
			print 'decoration is empty'
		return decoration
	def getHouseLabels(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("labels",category)
		results = hxs.xpath(xnode)
		labels = ''	
		for result in results:
			l = result.xpath('text()').extract()
			if l:
				labels = labels+l[0].strip()+' '
		if labels:
			print labels
		else:
			print 'labels is empty'
		return  labels			
	def getHouseDistrict(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("district",category)
		result = hxs.xpath(xnode).extract()
		district = ''
		if result:	
			district = result[0].strip()
		if district:
			print district
		else:
			print 'district is empty'
		return district
	def getHouseLocation(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("location",category)
		result = hxs.xpath(xnode).extract()
		location = ''
		if result:	
			location = result[0].strip()
		if location:
			print location
		else:
			print 'location is empty'
		return location			
	def getHouseHuxingPic(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("huxing_pic",category)
		result = hxs.xpath(xnode).extract()
		huxingPic = ''
		if result:	
			huxingPic = result[0].strip()
		if huxingPic:
			print huxingPic
		else:
			print 'huxingPic is empty'
		return huxingPic
	def getHousePicList(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("pic_list",category)
		results = hxs.xpath(xnode)
		L = range(1,len(results))
		for result in results:
			p = result.xpath('a/@href').extract()
			if p:
				print p[0]
				L.append(p[0])
		return L
	def getAgentTelephone(self,response,category):
		hxs = HtmlXPathSelector(response)
		xnode = self.getTemplate("telephone",category)
		result = hxs.xpath(xnode).extract()
		tel = ''
		if result:	
			tel = result[0].strip()
		else:
			print 'tel is empty'
		print tel
		return tel
	
	def getTemplate(self,node,category):
		""" 
		if apartment return 0 
	    if house return 1 
	    if shop return 2 
	    it is used for different pattern to analysis data from website
	    """
		model = {
					'title': (
						'//div[@class="title"]/h1/text()',
						), 
					'allprice': (
						'//dt[@class="gray6 zongjia1"]/span[2]/text()',
						),
					'square':(
						'//div[@class="base_info"]/dl[1]/dd[4]/span/text()',
						'//div[@class="base_info"]/dl[1]/dd[4]/span/text()',
						'//div[@class="base_info"]/dl[1]/dd[2]/strong/text()'
						),
					'layout':(
						'//div[@class="base_info"]/dl[1]/dd[3]/text()',
						),
					'age':(
						'//div[@class="base_info"]/dl[2]/dd[1]/text()',
						),
					'orientation':(
						'//div[@class="base_info"]/dl[2]/dd[2]/text()',
						),
					'floor':(
						'//div[@class="base_info"]/dl[2]/dd[3]/text()',
						'//div[@class="base_info"]/dl[2]/dd[3]/text()',
						'//div[@class="base_info"]/dl[2]/dd[1]/text()',
						),
					'decoration':(
						'//dl[@class="borderb mb10"]/dd[5]/text()',
						),
					'labels':(
						'//p[@class="note"]/span',
						),
					'district':(
						'//div[@class="base_info"]/dl[2]/dt[1]/a[1]/text()',
						),
					'location':(
						'//div[@class="traffic mt10"]/p/text()',
						),
					'huxing_pic':(
						'//div[@id="esfshxq_117"]/div/a/img/@src',
						),
					'pic_list':(
						'//div[@id="esfshxq_116"]/div',
						),
					'telephone':(
						'//span[@id="mobilecode"]/text()',
						)
				}
		if len(model[node]) >category:
			return model[node][category]
		else:
			return model[node][0]
	def getAgentTemplate(self,node,category):
		agent = {
			'name':(
				'//div[@class="rzname floatl"]/text()',
				'//div[@class="rzren"]/dl/dt/text()',
				),
			'tel' :(
				'//span[@class="phonenum"]/text()',
				),
			'company':(
				'//ul[@class="cont02 mb10"]/li[1]/text()',
				'//div[@class="rzxxL"]/dl/dd[1]/text()',
				),
			'circle':(

				),
			'store_name':(
				'//ul[@class="cont03"]/li[2]/text()',
				'',
				),
			'head_url':(
				'//div[@class="rzren"]/img/@src',
				'//div[@class="photo"]/a/img/@src',
				),
			'dom':(
				'//ul[@class="cont02 mb10"]/li',
				),
		}
