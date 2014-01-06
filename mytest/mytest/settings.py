# Scrapy settings for mytest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mytest'

SPIDER_MODULES = ['mytest.spiders']
NEWSPIDER_MODULE = 'mytest.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mytest (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
IMAGES_STORE = '/home/stephen/scrapy/mytest/images'
ITEM_PIPELINES = [
	# 'mytest.pipelines.MytestPipeline',
    'mytest.pipelines.MyImagesPipeline'
]
# ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}

MYSQL_HOST = '192.168.1.99'
MYSQL_DBNAME = 'house_spider'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'ikuaizu@205'
