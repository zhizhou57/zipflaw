# -*- coding: utf-8 -*-
# @Time    : 2024/9/18 12:08
# @Author  : 
# @File    : english_wiki_spider.py.py
import time
import scrapy
import html
from ..items import WikipediaEnglishItem
import re

class EnglishWikiSpider(scrapy.Spider):
    name = 'english_wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Natural_language_processing']  # Example starting page
    max_pages = 10000  # Set the maximum number of pages to crawl
    page_count = 0
    start_time = None

    # scrapy suppose removing duplicate urls

    def clean(self, text):
        # Unescape HTML entities (like &nbsp;, &lt;, &gt;)
        text = html.unescape(text)
        # Replace multiple spaces/newlines with a single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def parse(self, response):
        if self.start_time is None:
            self.start_time = time.time()

        self.page_count += 1    
        # Stop the spider when the page count reaches the maximum
        if self.page_count >= self.max_pages:
            self.crawler.engine.close_spider(self, reason='Reached maximum page limit')

        if self.page_count % 100 == 0:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            self.logger.info(f"Crawled {self.page_count} pages")
            self.logger.info(f"Time elapsed: {elapsed_time:.2f} seconds")

        # Extract title and text content from the Wikipedia page
        title = response.xpath('//*[@id="firstHeading"]/span/text()').get()
        paragraphs = response.xpath('//div[@id="bodyContent"]//p//text()').getall()
        content = " ".join(paragraphs)
        content = self.clean(content)

        item = WikipediaEnglishItem(title=title, content=content, url=response.url)
        yield item

        # Follow links to other Wikipedia pages
        for href in response.xpath('//div[@id="bodyContent"]//a/@href').getall():
            if href.startswith('/wiki/') and not ':' in href:  # Filter only article pages
                yield response.follow(href, callback=self.parse)
