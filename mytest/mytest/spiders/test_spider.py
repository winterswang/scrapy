from scrapy.spider import BaseSpider
from twisted.enterprise import adbapi 
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from mytest.items import ImageItem,Website
from datetime import datetime
from scrapy.http import Request
import MySQLdb
import urlparse
import re

class TestSpider(BaseSpider):
    name = "test_image"
    allowed_domains = ["bj.esf.sina.com.cn"]    
    start_urls = []

    def start_requests(self):
        result = self.getData()
        for l in result:
            request = Request(l, dont_filter=True)
            yield request

    def getData(self):
        try:
            conn=MySQLdb.connect(host='192.168.1.99',user='root',passwd='ikuaizu@205',db='house',port=3306,charset='utf8')
            cur=conn.cursor()
            cur.execute('select url from house_soufun limit 0,1')
            result=cur.fetchall()
            url = []
            for u in result:
              url.append(u[0])
            cur.close()
            conn.close()
            return url
        except MySQLdb.Error,e:
          print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def parse(self, response):

        body = response.body.decode('gbk', 'ignore').encode('utf-8')
        hxs = HtmlXPathSelector(response)
        items = []
        xnode = '//div[@class = "describe mt10"]//img[contains(@src,"jpg")]//@src'
        results = hxs.xpath(xnode)
        website = Website()
        website['house_id']   = self.getHouseId(response.url)
        for result in results:
            item = ImageItem()
            image_relative_url = result.extract()
            image_absolute_url = urlparse.urljoin(response.url, image_relative_url.strip())
            item['image_urls'] = [image_absolute_url]
            items.append(item)
        website['url'] = items
        return website

    def getHouseId(self,url):
        pattern = re.compile(r'shou/(.*).htm')
        match = pattern.search(url)
        result = ''
        if match:
            result = match.group(1)
        return result
