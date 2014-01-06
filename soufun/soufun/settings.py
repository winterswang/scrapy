# Scrapy settings for soufun project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'soufun'

SPIDER_MODULES = ['soufun.spiders']
NEWSPIDER_MODULE = 'soufun.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'soufun (+http://www.yourdomain.com)'
IMAGES_STORE = '/home/stephen/scrapy/soufun/images'
ITEM_PIPELINES = [
    'soufun.pipelines.SQLHousePipeline',
    'soufun.pipelines.SQLAgentPipeline',
    'soufun.pipelines.SQLQuestionPipeline',
    'scrapy.contrib.pipeline.images.ImagesPipeline'
]


MYSQL_HOST = '192.168.1.99'
MYSQL_DBNAME = 'house'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'ikuaizu@205'
