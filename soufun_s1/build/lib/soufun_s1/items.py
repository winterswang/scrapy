# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SoufunItem(Item):
	houseid     = Field()
	title       = Field()
	agent_tel   = Field()
	description = Field()
	pic_list	= Field()
	labels		= Field()
	total_price = Field()
	dicts       = Field()
	url         = Field()
	types       = Field()
	location    = Field()
