import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bekb.items import Article


class BekbSpider(scrapy.Spider):
    name = 'bekb'
    start_urls = ['https://www.bekb.ch/de/blog']

    def parse(self, response):
        links = response.xpath('//div[@class="rcw-c-blogteaser__row"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h3[@class="rcw-c-hero__lead"]/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="rcw-c-container__content"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
