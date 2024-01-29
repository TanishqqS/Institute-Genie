import scrapy
from scrapy.http import Response
from typing import Any
from ..items import ScrapeshikshaItem
import time
from urllib.parse import urljoin


class ShikshaSpider(scrapy.Spider):
    name = "Shiksha"
    start_urls = [
        "https://www.shiksha.com/engineering/ranking/top-engineering-colleges-in-india/44-2-0-0-0"
    ]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        uni_links = response.css('a.rank_clg.ripple.dark::attr(href)').extract()        #href links of the universities
        # yield {'href': href_links}
        for uni in uni_links:
            absolute_url = urljoin(response.url, uni)
            yield scrapy.Request(absolute_url, callback=self.parse_university)

    # this would partially work separately
    def parse_university(self, response: Response, **kwargs: Any) -> Any:
        href_links = response.css('li a.listItem.ripple.dark::attr(href)').extract()        #href links to the different tabs
        for href in href_links:                
            absolute_url = urljoin(response.url, href)
            yield scrapy.Request(absolute_url, callback=self.parse_page)

    def parse_page(self, response: Response, **kwargs: Any) -> Any:
        courses = response.css('div.c8ff h3::text').extract()
        review = response.css('div.rvwScore h3::text').extract()
        yield {'courses': courses, 'review': review}





