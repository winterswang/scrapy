# Scrapy settings for soufun_s1 project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'soufun_s1'

SPIDER_MODULES = ['soufun_s1.spiders']
NEWSPIDER_MODULE = 'soufun_s1.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'soufun_s1 (+http://www.yourdomain.com)'
ITEM_PIPELINES = [
    'soufun_s1.pipelines.SQLHousePipeline',
]

MYSQL_HOST = '192.168.1.99'
MYSQL_DBNAME = 'house'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'ikuaizu@205'