# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpenriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # restaurant_name = scrapy.Field()
    user_review = scrapy.Field()
    # restaurant_url = scrapy.Field()
    
    
