# -*- coding: utf-8 -*-
import scrapy
from .. import items


class ExampleSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["demoz.org"]
    start_urls = (
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
    )

    def parse(self, response):
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//ul/li')
        web_items = []
        for site in sites:
            item = items.TutorialItem()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').re('-\s([^\n]*?)\\n')
            web_items.append(item)
        return web_items

