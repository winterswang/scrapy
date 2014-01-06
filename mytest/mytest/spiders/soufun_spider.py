
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from mytest.items import SoufunItem
from scrapy import log
import re


class DmozSpider(CrawlSpider):
    name = "soufun_agent"
    allowed_domains = ["soufun.com"]
    start_urls = [ 
        "http://esf.sh.soufun.com/agenthome/",
        "http://esf.gz.soufun.com/agenthome/",
        "http://esf.sz.soufun.com/agenthome/",
    ]   
    rules = [Rule(SgmlLinkExtractor('soufun.com/agenthome-.*'), callback='parse_item_store', follow=True)]

    def parse_item_store(self, response):
        pattern = re.compile(r'pingjiaagent\(\'.+?\)', re.M) 
        body = response.body.decode('gbk', 'ignore').encode('utf-8')
        items = []
        for l in pattern.finditer(body):
            info = l.group()
            strlist = info.split(',')
            item['city'] = self.get_city(response.url)
            item['name'] = strlist[1].strip()[1:-1].strip()
            item['head_url'] =strlist[5].strip()[1:-1].strip()
            item['tel']  = strlist[2].strip()[1:-1].strip()
            item['company'] = strlist[4].strip()[1:-1].strip()
            item['store_url'] = self.get_store_url(response.url,strlist[3].strip()[1:-1].strip())
            item['store_name'] = ''
            items.append(item)
        return items

    def get_city(self,url):
        pattern = re.compile(r'esf\.(\w+)\.soufun', re.M)
        lists =  pattern.finditer(url)
        for l in lists: 
            info = l.group()
            strlist = info.split('.')
            city = strlist[1]
            if city == 'sh':
                return 'shanghai'
            if city == 'gz':
                return 'guangzhou'
            if city == 'sz':
                return 'shenzhen'
            else:
                return 'beijing'
                
    def get_store_url(self,url,store_id):
        pattern = re.compile(r'esf(.*)\.com', re.M)
        lists =  pattern.finditer(url)
        for l in lists:
            info =  l.group()
            return  info+'/a/'+store_id


