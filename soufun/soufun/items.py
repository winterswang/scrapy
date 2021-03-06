# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class AgentItem(Item):
	name        = Field()
	agent_tel   = Field()
	company     = Field()
	circle      = Field()
	head_url    = Field()
	store_name  = Field()
	store_url	= Field()
	city        = Field()	

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
	store_url   = Field()

class QuestionItem(Item):
	question = Field()
	answer   = Field()
class ImageItem(Item):
    image_urls  = Field()
    images      = Field()