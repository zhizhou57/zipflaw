# -*- coding: utf-8 -*-
# @Time    : 2024/9/19 18:50
# @Author  : yesliu
# @File    : chinese_wiki_spider.py.py
import time
import scrapy
import html
from ..items import WikipediaChineseItem
import re

class ChineseWikiSpider(scrapy.Spider):
    name = 'chinese_wiki'
    allowed_domains = ['zh.wikipedia.org']
    start_urls = ['https://zh.wikipedia.org/wiki/自然语言处理']  # Example starting page
    max_pages = 40000  # Set the maximum number of pages to crawl
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

        item = WikipediaChineseItem(title=title, content=content, url=response.url)
        yield item

        # Follow links to other Wikipedia pages
        for href in response.xpath('//div[@id="bodyContent"]//a/@href').getall():
            if href.startswith('/wiki/') and not ':' in href:  # Filter only article pages
                yield response.follow(href, callback=self.parse)
