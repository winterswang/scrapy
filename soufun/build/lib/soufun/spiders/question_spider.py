# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from soufun.items import QuestionItem
from HTMLParser import HTMLParser
from scrapy import log
import sys
import re
class question_spider(CrawlSpider):
	name = 'question'
	allowed_domains = ["yzddtk.com"]
	start_urls = ["http://www.yzddtk.com/tiku/"]
	rules = [
		Rule(SgmlLinkExtractor(allow=('http://www.yzddtk.com/yizhandaodi.*html$'),restrict_xpaths=('//div[@id="portal_block_61_content"]')), callback='parse_item',follow=True)	
	]

	def parse_item(self,response):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		hxs = HtmlXPathSelector(response)
		questions = hxs.xpath('//div[@class="t_fsz"]//td/text()').extract()
		items = []
		for q in questions:
			q = q.replace('、',' ').replace('：',' ').replace('.',' ').replace('“',' ')
			lists =  q.split('？')
			if len(lists) == 2:
				strs =  lists[0].split(' ')
				res = lists[0].replace(strs[0],'')
				print res.strip()
				print lists[1].strip()
				item = QuestionItem()
				item['question'] = res.strip()
				item['answer']   = lists[1].strip()
				items.append(item)
		return items
