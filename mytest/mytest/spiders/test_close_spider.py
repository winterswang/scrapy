# encoding: utf-8
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.selector import HtmlXPathSelector
from mytest.items import SoufunItem
from scrapy import log
import sys
import re

class testCloseSpider(CrawlSpider):
    name = "testclose"
    allowed_domains = ["esf.sina.com.cn"]
    start_urls = [
        # "http://bj.esf.sina.com.cn/agent/",
        # "http://sh.esf.sina.com.cn/agent/",
        # "http://gz.esf.sina.com.cn/agent/",
        "http://sz.esf.sina.com.cn/agent/",
    ]
    rules = [
        Rule(SgmlLinkExtractor('esf.sina.com.cn/agent/n\d+/$'), callback='parse_item')
    ]

    def __init__(self, level=None, *args, **kwargs):
    	super(testCloseSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print 'i am closing'

    def parse_item(self, response):
        body = response.body.decode('gbk', 'ignore').encode('utf-8')
        hxs = HtmlXPathSelector(response)
        items = []
        reload(sys)
        sys.setdefaultencoding('utf-8')
        city = self.get_city(response.url)
        lists = hxs.xpath('//div[@class="broker-lists-item"]')
        for l in lists:
          name = ''
          pic  = ''
          tel  = ''
          store_url = ''
          store_name = ''
          ##################################
          # name = hxs.xpath('//div[@class="title"]/div[@class="name"]/text()').extract()
          # pic =  hxs.xpath('//div[@class="photo"]/img/@src').extract()
          # tel = hxs.xpath('//div[@class="about"]/li[3]/text()').extract()
          # company =  hxs.xpath('//div[@class="about"]/li[4]/a/text()').extract()
          # store_name = hxs.xpath('//div[@class="about"]/li[5]/text()').extract()
          ##################################
          name = l.xpath('dl/dd[1]/p[1]/strong/a/text()').extract()
          pic  = l.xpath('dl/dt/a/img/@src').extract()
          store_url = l.xpath('dl/dd[2]/p[1]/a/@href').extract()

          ps = l.xpath('dl/dd[1]/p')

          for p in ps:
            body = str(p.extract()).encode('utf-8')

            pattern = re.compile(ur'服务区域：(\w+)', re.U)
            result = pattern.finditer(unicode(body))
            for l in result:
              circle = l.group()

            pattern = re.compile(ur'所属门店：\w+', re.U)
            result = pattern.finditer(unicode(body))
            for l in result:
              store_name = l.group()


            pattern = re.compile(r'\d{11,}', re.M)
            result = pattern.finditer(unicode(body))
            for l in result:
              tel = l.group()
            
          if  name and tel:
              item = SoufunItem()
              item['name'] = name[0] 
              item['head_url'] = pic[0]
              item['city'] = city
              item['tel'] = tel
              item['company'] = ''
              item['circle'] =circle
              item['store_name'] = store_name
              item['store_url'] = store_url[0]
              items.append(item)
        # return items

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