# encoding: utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.contrib.pipeline.images import ImagesPipeline
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
from scrapy import log
from baidumap import xBaiduMap
from scrapy.http import Request
import sys
import hashlib
import time

class SoufunS1Pipeline(object):
    def process_item(self, item, spider):
        return item

class SQLHousePipeline(object):

    def __init__(self,my_settings):
        # start the spider then get the start time to check the house update situation
        self.now = int(time.time())
        self.my_settings = my_settings
        self.dbpool = self.getDBpool();
        reload(sys)
        sys.setdefaultencoding('utf-8')
    @classmethod
    def from_settings(cls,settings):
        my_settings = {
                    "host":settings.get("MYSQL_HOST"),
                    "dbname":settings.get("MYSQL_DBNAME"),
                    "user":settings.get("MYSQL_USER"),
                    "passwd":settings.get("MYSQL_PASSWD"),
                    "pic_address":settings.get("IMAGE_ADDRESS"),
                    }       
        return cls(my_settings)   

    # def __init__(self, dbpool):
    #     self.dbpool = dbpool
    #     reload(sys) 
    #     sys.setdefaultencoding('utf-8')

    # @classmethod
    # def from_settings(cls, settings):
    #     dbargs = dict(
    #         host=settings['MYSQL_HOST'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         passwd=settings['MYSQL_PASSWD'],
    #         charset='utf8',
    #         use_unicode=True,
    #     )
    #     dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
    #     return cls(dbpool)

    def getDBpool(self):
        dbargs = dict(
            host=self.my_settings['host'],
            db=self.my_settings['dbname'],
            user=self.my_settings['user'],
            passwd=self.my_settings['passwd'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return dbpool        
    def process_item(self, item, spider):
        if item.has_key('house_id'):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item
 
    def _conditional_insert(self, tx, item):
        lng = 0.0
        lat = 0.0
        if item['location']:
            location = self.getLocation(item['location'],'上海')
            if location and len(location) ==2:
                lat = float(location[0])
                lng = float(location[1])

        tx.execute("select * from house_soufun where house_id =%s and agent_open_id =%s", (item['house_id'],item['open_id']))

        data = [item['house_id'],item['title'],item['description'],item['agent_tel'], item['url'],item['types'],item['labels'],item['location'],self.now,item['store_url'],lat,lng,item['open_id']]
        result = tx.fetchone()
        # if find the result by agent_open_id, then ,update the data,the column now can specify the house data is new or have sold 
        if result:
            data.append(item['house_id'])
            tx.execute(
                "update house_soufun set house_id=%s,title=%s, description=%s, agent_tel=%s,url=%s,house_type=%s,labels=%s,location=%s,createtime=%s,store_url=%s,lat=%s,lng=%s where agent_open_id =%s and house_id=%s" ,data
            )
            self.update_agent_store_updatecount(tx,item['store_url'])
            log.msg("house updated in db: %s" % item, level=log.DEBUG)

        #insert into the house_soufun, agent_open_id is the key  
        else:
            tx.execute(
                "insert into house_soufun (house_id, title, description, agent_tel,url,house_type,labels,location,createtime,store_url,lat,lng,agent_open_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , data
            )
            self.update_agent_store_insertcount(tx,item['store_url'])
            log.msg("house inserted in db: %s" % item, level=log.DEBUG)
        #update or insert into house_photo
        self._save_house_photo(tx, item['open_id'],item['house_id'],item['pic_list'])
        self._save_house_desc(tx, item['open_id'],item['house_id'],item['dicts'])

    def _save_house_photo(self, tx, agent_open_id, house_id, photoes):
        table = 'soufun_house_photo_'+house_id[len(house_id)-1:len(house_id)]
        bad_image = 'http://img.soufun.com/rent/image/jubaoImg01.png'
        for p in photoes:
            for photo_url in p['image_urls']:
                if photo_url != bad_image:
                    tx.execute("select * from "+table+" where agent_open_id = %s and photo_url= %s ", (agent_open_id,photo_url))
                    result = tx.fetchone()
                    pic_url =self.my_settings['pic_address']+hashlib.sha1(photo_url).hexdigest()+".jpg"
                    data = (house_id, photo_url,pic_url,agent_open_id)
                    #check the photo_url is in database or not ,if yes, then check pic_url is in or not
                    # if the photo_url is not in database, then ,insert into the database
                    if result:
                        #check pic_url is null if null update the pic_url
                        if not result[3] or result[3] =='':
                            tx.execute("update "+table+" set pic_url=%s where house_id =%s and photo_url = %s and agent_open_id =%s", data)
                            log.msg("pic_url have stored in db", level=log.DEBUG)

                        # if the pic_url is in database then print the log and do nothin    
                        log.msg("photos have stored in db", level=log.DEBUG)
                    else: 
                        # if the photo_url and agent_open_id is not in database ,then ,insert the house_id,photo_url,pic_url,agent_open_id in database                 
                        tx.execute("insert into "+table+" (house_id, photo_url, pic_url, agent_open_id) values(%s,%s,%s,%s)", data)
                        log.msg("photos have inserted in db", level=log.DEBUG)

    def _save_house_desc(self, tx, agent_open_id, house_id, descs):
        for (k,v) in descs.items():
            # check the house_desc(every key and value) of the agent is in database
            # if in ,update the data,if not ,insert into the database
            tx.execute("select * from soufun_house_desc where house_id = %s and agent_open_id = %s and `key`=%s and `value` =%s", (house_id,agent_open_id,k,v))
            result = tx.fetchone()
            data = (house_id, k, v,agent_open_id)     
            if result:
                tx.execute("update soufun_house_desc set house_id= %s, `key`=%s, `value`=%s where agent_open_id = %s",data)
                log.msg("house_desc have stored in db", level=log.DEBUG)       
            else:
                tx.execute('insert into soufun_house_desc (house_id, `key`, `value`, agent_open_id) values(%s,%s,%s,%s)', data)
                log.msg("house_desc have inserted in db", level=log.DEBUG)       

    def update_agent_store_updatecount(self,tx,store_url):
        tx.execute("select update_count from agent_store where store_url=%s",store_url)
        result = tx.fetchone()
        if result:
            data = [int(result[0])+1,store_url]
            tx.execute("update agent_store set update_count =%s where store_url =%s",data)
            log.msg("update_count update successful", level=log.DEBUG)
        else:
            log.msg("get update_count failed", level=log.DEBUG)   

    def update_agent_store_insertcount(self,tx,store_url):
        tx.execute("select insert_count from agent_store where store_url=%s",store_url)
        result = tx.fetchone()
        if result:
            data = [int(result[0])+1,store_url]
            tx.execute("update agent_store set insert_count =%s where store_url =%s",data)
            log.msg("insert_count update successful", level=log.DEBUG)
        else:
            log.msg("get insert_count failed", level=log.DEBUG)
    
    def getLocation(self,location,city):
        bm=xBaiduMap()
        return bm.getLocation(location,city)

    def handle_error(self, e):
        log.err(e)
        # conn = self.dbpool.connections.get(self.threadID())
        # self.dbpool.disconnect(conn)
        # try the interaction again
        self.dbpool = self.getDBpool();

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item.has_key('pic_list'):
            for image_item in item['pic_list']:
                for image_url in image_item['image_urls']:
                    if image_url !='http://img.soufun.com/rent/image/jubaoImg01.png':
                        yield Request(image_url)

    def item_completed(self, results, item, info):

        return item

class SQLAgentPipeline(object):
 
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)
 
    def process_item(self, item, spider):
        print spider.name
        if item.has_key('city') and item.has_key('store_url'):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item    
        # else:
        #     return    
        #     # raise DropItem("not agent pipeline")


 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        now = int(time.time())
        tx.execute("select * from agent_soufun where store_url = %s", (item['store_url'],))
        result = tx.fetchone()
        data = [item['name'],item['agent_tel'],item['company'],item['circle'], item['head_url'],item['store_name'],item['city'],item['store_url']]
        if result:
            data.append(item['store_url'])
            tx.execute(
                "update agent_soufun set name=%s,agent_tel=%s, company=%s, circle=%s,head_url=%s,store_name=%s,city=%s,store_url=%s where store_url =%s" , data
            ) 
            log.msg("Item updated in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute(
                "insert into agent_soufun (name, agent_tel, company, circle,head_url,store_name,city,store_url) values (%s,%s,%s,%s,%s,%s,%s,%s)" , data
            )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)