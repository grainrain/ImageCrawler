from datetime import datetime

import scrapy

from ImageCrawler.items import ImagecrawlerItem


class ImagecrawlerspiderSpider(scrapy.Spider):
    name = "ImageCrawlerSpider"
    allowed_domains = ["taiav.com"]

    def start_requests(self):
        urls = [
            'https://taiav.com/discover'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(20 * "-", '视频分类', 20 * "-")
        records = response.xpath("//div[contains(@class,'uk-grid-small')]//div")
        for record in records:
            parent_title = record.xpath("./a/text()").extract_first()
            parent_title = str(parent_title).replace("·", "")
            parent_url = record.xpath("./a/@href").extract_first()
            parent_url = response.urljoin(parent_url)
            # print(parent_title, '/', url)
            yield scrapy.Request(url=parent_url, callback=self.parse_child, meta={'parent_title': parent_title})


    def parse_child(self, response):
        parent_title = response.meta['parent_title']
        videos = response.xpath("//div[contains(@class,'uk-card-hover')]")

        for video in videos:
            video_url = video.xpath("./div[contains(@class,'uk-card-body')]/a/@href").extract_first()
            title = video.xpath("./div[contains(@class,'uk-card-media-top')]//img/@alt").extract_first()
            image_url = video.xpath("./div[contains(@class,'uk-card-media-top')]//img/@src").extract_first()
            publish_date = video.xpath(".//a//div[contains(@class,'video-box-info')]/div[1]/text()").extract_first()
            if "GMT" in publish_date:
                publish_date = publish_date[0:publish_date.index("GMT")].strip()
                GMT_FORMAT = '%a %b %d %Y %H:%M:%S'
                publish_date = datetime.strptime(publish_date, GMT_FORMAT)
                publish_date = str(publish_date)[0:str(publish_date).index(" ")]
            else:
                publish_date = str(publish_date)[0:str(publish_date).index("T")]

            hits = video.xpath(".//a//div[contains(@class,'video-box-info')]/div[2]/text()[2]").extract_first()
            hits = str(hits).strip()
            image_url = response.urljoin(image_url)
            video_url = response.urljoin(video_url)
            image_urls = list()
            image_urls.append(image_url)
            # print(image_urls, '/', publish_date, '/', hits, '/', title, '/', video_url)
            if len(title) > 40:
                title = title[0:40]
            print(image_urls, '/', publish_date, '/', hits, '/', title)
            imagecrawlerItem = ImagecrawlerItem()
            imagecrawlerItem["publish_date"] = str(publish_date)
            imagecrawlerItem["hits"] = str(hits)
            imagecrawlerItem["image_urls"] = image_urls
            imagecrawlerItem["title"] = title
            imagecrawlerItem["parent_title"] = parent_title
            imagecrawlerItem["video_url"] = video_url
            yield imagecrawlerItem

        next_page = response.xpath("//ul[contains(@class,'pagination')]/li[last()]/a/@href").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse_child, meta={'parent_title': parent_title})
        pass
