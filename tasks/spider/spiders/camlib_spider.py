import sys
import scrapy
from spider.items import Book

# Javascript action from the 'AVAILABILITY' filter button
AVAILABILITY_URL = "javascript:subform('addfacet#AvailableLicence:(%2238%22)#Availability:  &amp; authid &amp; ','searchresults_basic2.asp')"

class CamlibSpider(scrapy.Spider):
    name = "camlib"
    allowed_domains = ["cambridgeshire.libraryebooks.co.uk"]

    def __init__(self, genre, *args, **kwds):
        self.genre = genre
        super(CamlibSpider, self).__init__(*args, **kwds)

    def start_requests(self):
        print "\nCrawling Genre '%s'" % self.genre["name"],
        sys.stdout.flush()
        return [scrapy.Request(self.genre["url"],
                                     self.parse_genre_crawl_next_page,
                                     # All requests redirect to the same URL, so don't filter duplicates
                                     dont_filter=True)]

    def parse_genre_crawl_next_page(self, response):
        """Scrape all of the books in the results, then crawl to the next page"""
        # TODO: Handle single-item result page
        if "catpage3.asp" in response.url:
            print "\bX",
            sys.stdout.flush()
            return
        print "\b.",
        sys.stdout.flush()
        for book in response.xpath("//ul[@class='cat_details']"):
            title = book.xpath(".//p[@class='small_title']/a/text()").extract_first()
            isbn = _isbn_from_url(book.xpath(".//p[@class='small_title']/a/@href").extract_first())
            author = book.xpath(".//li[@class='author']/text()").extract_first()
            cover_url = book.xpath(".//li[@class='b_cover']/div/a/img/@src").extract_first()
            in_stock = book.xpath(".//p[@class='inStock']")
            genre = self.genre["name"]
            if in_stock:
                yield Book(title=title,
                           isbn=isbn,
                           author=author,
                           cover_url=cover_url,
                           genre=genre)

        next_page_url = response.xpath("//a[@title='Show next page of results']/@href").extract_first()
        if next_page_url:
            formdata = _form_data_from_url(next_page_url)
            yield scrapy.FormRequest.from_response(response,
                                    formxpath="//form[@name='s_results_form']",
                                    formdata=formdata,
                                    meta=response.meta,
                                    callback=self.parse_genre_crawl_next_page,
                                    # All requests redirect to the same URL, so don't filter duplicates
                                    dont_filter=True)

def _isbn_from_url(url):
    """Example url: catpage3.asp?isbn=9781409087243-6"""
    tail = url.split("isbn=")[1]
    isbn = tail.split("-")[0]
    return isbn

def _form_data_from_url(url):
    """Example url: javascript:subform('resultpage','/site/EB/ebooks/searchresults_basic2.asp?mp_startno=20')"""
    _, state, _, target, _ = url.split("'")
    return {"state": state, "target": target}
