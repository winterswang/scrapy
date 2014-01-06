# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
class SoufunPipeline(object):
    def process_item(self, item, spider):
        return item
        
class SQLHousePipeline(object):
 
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
        if item.has_key('houseid'):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item
        # else:
            # raise DropItem("not house pipeline")


 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        tx.execute("select * from house_soufun where house_id = %s", (item['houseid'],))
        data = [item['houseid'],item['title'],item['description'],item['agent_tel'], item['url'],item['types'],item['labels'],item['location'],now]
        result = tx.fetchone()
        if result:
            data.append(item['houseid'])
            tx.execute(
                "update house_soufun set house_id=%s,title=%s, description=%s, agent_tel=%s,url=%s,house_type=%s,labels=%s,location=%s,createtime=%s where house_id=%s" ,data
            ) 
            log.msg("Item updated in db: %s" % item, level=log.DEBUG)
        else:
            tx.execute(
                "insert into house_soufun (house_id, title, description, agent_tel,url,house_type,labels,location,createtime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" , data
            )
            self._save_house_photo(tx, item['houseid'],item['pic_list'])
            self._save_house_desc(tx, item['houseid'],item['dicts'])
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
    def _save_house_photo(self, tx, house_id, photoes):
        for p in photoes:
            tx.execute("select * from soufun_house_photo where house_id = %s and photo_url=%s", (house_id,p))
            result = tx.fetchone()
            if result:
                log.msg("Item have stored in db", level=log.DEBUG)
            else:         
                data = (house_id, p)
                tx.execute('insert into soufun_house_photo(house_id, photo_url) values(%s,%s)', data)

    def _save_house_desc(self, tx, house_id, descs):
        for (k,v) in descs.items():
            tx.execute("select * from soufun_house_desc where house_id = %s and `key`=%s and `value` =%s", (house_id,k,v))
            result = tx.fetchone()     
            if result:
                log.msg("Item have stored in db", level=log.DEBUG)       
            data = (house_id, k, v)
            tx.execute('insert into soufun_house_desc(house_id, `key`, `value`) values(%s,%s,%s)', data)

    def handle_error(self, e):
        log.err(e)

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
        if item.has_key('store_url'):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item    
        # else:
        #     return    
        #     # raise DropItem("not agent pipeline")


 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
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

class SQLQuestionPipeline(object):
 
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host='192.168.1.99',
            db='test',
            user='root',
            passwd='ikuaizu@205',
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)
 
    def process_item(self, item, spider):
        if item.has_key('question'):
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
        return item
        # else: 
        #     return    
        #     # raise DropItem("not question pipeline")


 
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist. 
        # all this block run on it's own thread
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        tx.execute("select * from question where question = %s", (item['question'],))
        result = tx.fetchone()
        data = ( item['question'],item['answer'])
        if result:

            log.msg("Item inserted in db: %s" % item, level=log.DEBUG)

        else: 
            tx.execute(
                "insert into question (question, answer) values (%s,%s)" , data
            )
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)