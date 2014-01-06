# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Website(Item):

    house_id    = Field()
    url         = Field()

class DoubanItem(Item):
    groupName      = Field()
    groupURL       = Field()
    totalNumber    = Field()
    relativeGroups = Field()
    activeUsers    = Field()

class SoufunItem(Item):
    name       = Field()
    tel        = Field()
    company    = Field()
    city       = Field()
    circle     = Field()
    store_url  = Field()
    store_name = Field()
    head_url   = Field()

class HouseItem(Item):
    houseid     = Field()
    title       = Field()
    allprice    = Field()
    square      = Field()
    layout      = Field()
    age         = Field()
    orientation = Field()
    floor       = Field()
    decoration  = Field()
    labels      = Field()
    district    = Field()
    location    = Field()
    description = Field()
    huxing_pic  = Field()
    pic_list    = Field()
    agent_tel   = Field()
    agent_store = Field()

class ImageItem(Item):
    image_urls  = Field()
    images      = Field()
    
	
