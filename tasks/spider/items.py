# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Book(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    cover_url = scrapy.Field()
    isbn = scrapy.Field()
    genre = scrapy.Field()
    rating = scrapy.Field()
