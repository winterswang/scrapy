# Scrapy settings for soufun_s1 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
from datetime import *

BOT_NAME = 'soufun_s2'

SPIDER_MODULES = ['soufun_s2.spiders']
NEWSPIDER_MODULE = 'soufun_s2.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'soufun_s2 (+http://www.yourdomain.com)'
IMAGE_ADDRESS = "housephoto/"++str(date.today())+"/full/"
IMAGES_STORE = '/home/stephen/vsfoufang/kz_www/apps/apiport/wwwroot/data/attachment/housephoto/'+str(date.today())
ITEM_PIPELINES = [
    'soufun_s2.pipelines.SQLHousePipeline',
    'soufun_s2.pipelines.MyImagesPipeline',
    'soufun_s2.pipelines.SQLAgentPipeline',
]

MYSQL_HOST = '192.168.1.99'
MYSQL_DBNAME = 'house'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'ikuaizu@205'
