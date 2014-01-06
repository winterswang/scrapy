# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from HTMLParser import HTMLParser
from soufun.items import AgentItem
from scrapy import log
import sys
import re
class soufun_agent_spider(CrawlSpider):
	name = 'soufun_agent'
	allowed_domains = ["soufun.com"]
	start_urls = ["http://esf.soufun.com/agenthome/-i31-j310/"]
	rules = [
		Rule(SgmlLinkExtractor(allow=('/agenthome.*/$')),follow=True),
		Rule(SgmlLinkExtractor(allow=('/a/.*')), callback='parse_item_agent',follow=True)	
	]

	def parse_item_agent(self,response):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		item = AgentItem()
		hxs = HtmlXPathSelector(response)
		name = hxs.xpath('//div[@class="rzname floatl"]/text()').extract()
		item['name'] = ''
		if name:
			item['name'] = name[0]
		else:
			name = hxs.xpath('//div[@class="rzren"]/dl/dt/text()').extract()
			if name:
				item['name'] = name[0]

		item['agent_tel'] = ''
		tel = hxs.xpath('//span[@class="phonenum"]/text()').extract()
		if tel:
			item['agent_tel'] =  tel[0]

		item['company']  = ''
		company = hxs.xpath('//ul[@class="cont02 mb10"]/li[1]/text()').extract()
		if len(company)>1:
			item['company'] =  company[1].replace('：','')
		else:
			company = hxs.xpath('//div[@class="rzxxL"]/dl/dd[1]/text()').extract()
			if company:
				item['company'] =  company[0]

		item['store_name'] = ''
		store_name =  hxs.xpath('//ul[@class="cont03"]/li[2]/text()').extract()
		if store_name:
			item['store_name'] = store_name[0]

		item['head_url'] = ''
		head_url = hxs.xpath('//div[@class="rzren"]/img/@src').extract()
		if head_url:
			item['head_url'] = head_url[0]
		else:
			head_url = hxs.xpath('//div[@class="photo"]/a/img/@src').extract()
			if head_url:
				item['head_url'] = head_url[0]

		item['circle'] = ''
		dom = hxs.xpath('//ul[@class="cont02 mb10"]/li')
		for d in dom:			
			body = str(d.extract()).encode('utf-8')
			pattern = re.compile(ur'服务商圈：(\w+([,]?\w+){1,})', re.U)
			result = pattern.search(unicode(body))
			if result:
				item['circle'] =  result.group(1)
		item['store_url'] = response.url
		item['city'] = self.get_city(response.url)
		return item	

	def get_city(self,url):
		pattern = re.compile(r'esf.(\w+).soufun', re.M)
		ll =  pattern.search(url)
		if ll: 
			city = ll.group(1)
			if city == 'sh':
				return 'shanghai'
			if city == 'gz':
				return 'guangzhou'
			if city == 'sz':
				return 'shenzhen'
			else:
				return city
		else:
			return 'beijing'