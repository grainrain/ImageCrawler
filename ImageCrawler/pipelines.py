# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import re
import time
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum

from ImageCrawler.settings import IMAGES_STORE


class DownloadImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        title = item['title']
        publish_date = item['publish_date']
        parent_title = item['parent_title']
        hits = item['hits']
        img_name = f"{parent_title}/{title}_{publish_date}_{hits}.jpg"
        return img_name

class CsvPipeline(object):
    def __init__(self):
        store_file = IMAGES_STORE + '/ImageCrawler.csv'
        self.file = open(store_file, 'a+', encoding="utf-8",newline = '')
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        self.writer.writerow([item['title'], item['hits'], item['publish_date'],item['video_url'], item['image_urls']])
        return item

    def close_spider(self, spider):
        self.file.close()

class ImagecrawlerPipeline:
    def process_item(self, item, spider):
        return item
