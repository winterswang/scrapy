from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from mytest.items import SoufunItem
from scrapy import log
import re

class AJKSpider(CrawlSpider):
    name = "anjuke"
    allowed_domains = ["anjuke.com"]
    start_urls = [
        # "http://bj.esf.sina.com.cn/agent/",
        # "http://sh.esf.sina.com.cn/agent/",
        "http://shanghai.anjuke.com/tycoon/",
        "http://guangzhou.anjuke.com/tycoon/",
    ]

    rules = [
        # Rule(SgmlLinkExtractor('esf.sina.com.cn/shop/.*'), callback='parse_item'),
        Rule(SgmlLinkExtractor('esf.sina.com.cn/agent/.*'), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        body = response.body.decode('gbk', 'ignore').encode('utf-8')
        hxs = HtmlXPathSelector(response)
        items = []

        city = self.get_city(response.url)
        lists = hxs.xpath('//div[@class="broker-lists-item"]')
        for l in lists:
          item = SoufunItem()
          ##################################
          # name = hxs.xpath('//div[@class="title"]/div[@class="name"]/text()').extract()
          # pic =  hxs.xpath('//div[@class="photo"]/img/@src').extract()
          # tel = hxs.xpath('//div[@class="about"]/li[3]/text()').extract()
          # company =  hxs.xpath('//div[@class="about"]/li[4]/a/text()').extract()
          # store_name = hxs.xpath('//div[@class="about"]/li[5]/text()').extract()
          ##################################

          name = l.xpath('dl/dd[1]/p[1]/strong/a/text()').extract()
          pic  = l.xpath('dl/dt/a/img/@src').extract()
          tel  = l.xpath('dl/dd[1]/p[5]/span/text()').extract()
          circle = l.xpath('dl/dd[1]/p[3]/text()').extract()
          company =  ''
          store_name = l.xpath('dl/dd[1]/p[4]/text()').extract()
          ####################################################
          store_url = l.xpath('dl/dd[2]/p[1]/a/@href').extract()
          # if name and tel:
          #   print name[0]
          #   print pic[0]
          #   print city
          #   print tel[0]
          #   print company
          #   print store_name[0]
          #   print store_url[0]     
          if name and tel:
                item['name'] = name[0] 
                item['head_url'] = pic[0]
                item['city'] = city
                item['tel'] = tel[0]
                item['company'] = ''
                item['store_name'] = store_name[0]
                item['store_url'] = store_url[0]
          items.append(item)
        return items

    def get_city(self,url):
      pattern = re.compile(r'(\w+)\.esf\.sina', re.M)
      lists =  pattern.finditer(url)
      for l in lists: 
          info = l.group()
          strlist = info.split('.')
          city = strlist[0]
          if city == 'sh':
              return 'shanghai'
          if city == 'gz':
              return 'guangzhou'
          if city == 'sz':
              return 'shenzhen'
          if city == 'bj':
              return 'beijing'