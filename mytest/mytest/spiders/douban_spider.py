
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from mytest.items import DoubanItem
import re

class GroupTestSpider(BaseSpider):
	name = "douban"
	allowed_domains = ["douban.com"]
	start_urls = [
		"http://www.douban.com/group/WHV/",
	]

	def __get_id_from_group_url(self, url):
		m =  re.search("^http://www.douban.com/group/([^/]+)/$", url)
		if(m):
			return m.group(1) 
		else:
			return 0

	def parse(self, response):
	
		open("douban",'wb').write(response.body)	
		self.log("Fetch group home page: %s" % response.url)

		hxs = HtmlXPathSelector(response)
		item = DoubanItem()

		#get group name
		item['groupName'] = hxs.xpath('//h1/text()').re("^\s+(.*)\s+$")[0]

		#get group id 
		item['groupURL'] = response.url
		groupid = self.__get_id_from_group_url(response.url)

		#get group members number
		members_url = "http://www.douban.com/group/%s/members" % groupid
		members_text = hxs.xpath('//a[contains(@href, "%s")]/text()' % members_url).re("\((\d+)\)")
		item['totalNumber'] = members_text[0]

		#get relative groups
		item['relativeGroups'] = []
		groups = hxs.select('//div[contains(@class, "group-list-item")]')
		for group in groups:
			url = group.xpath('div[contains(@class, "title")]/a/@href').extract()[0]
			item['relativeGroups'].append(url)
		#item['relativeGroups'] = ','.join(relative_groups)
		return item
