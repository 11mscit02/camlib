import scrapy
from spider.items import Genre

class GenreSpider(scrapy.Spider):
    name = "genre"
    allowed_domains = ["cambridgeshire.libraryebooks.co.uk"]
    start_urls = ['http://cambridgeshire.libraryebooks.co.uk/site/EB/ebooks/genre.asp']

    def parse(self, response):
        """From the genre selection page, return the list of genres"""
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        for genre_obj in response.xpath("//ul[@class='genreList']//li"):
            name = genre_obj.xpath("a/text()").extract_first()
            relative_url = genre_obj.xpath("a/@href").extract_first()
            url = response.urljoin(relative_url)
            book_count = int(genre_obj.xpath("a/following-sibling::text()").extract_first()[2:-1])
            yield Genre(name=name, url=url, book_count=book_count)
