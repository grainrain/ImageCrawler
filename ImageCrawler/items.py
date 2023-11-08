# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagecrawlerItem(scrapy.Item):
    image_urls = scrapy.Field()
    publish_date = scrapy.Field()
    title = scrapy.Field()
    hits = scrapy.Field()
    parent_title = scrapy.Field()
    video_url = scrapy.Field()
    pass
