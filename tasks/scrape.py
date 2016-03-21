#!/usr/bin/env python
"""

* Scrape books from Cambridgeshire Library eBooks website
* Add ratings from GoodReads.com
* Serve up with Flask
"""
import os
import json
from time import sleep
import logging
logging.basicConfig()

from twisted.internet import reactor, defer
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from spider.spiders.camlib_spider import CamlibSpider
from rating import goodreads

GENRE_LIST = ["Biography & True Stories",
              "Fiction & related items",
              "Mathematics & science",
              ]

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT = os.path.join(THIS_DIR, "..", "_json", "camlib.json")

def run_spider():
    books = []
    def add_item(item):
        books.append(dict(item))

#    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        for genre in GENRE_LIST:
            crawler = Crawler(CamlibSpider, settings)
            crawler.signals.connect(add_item, signals.item_passed)
            yield runner.crawl(crawler, genre=genre)
        reactor.stop()
        print

    crawl()
    reactor.run()
    print "Collected %d books" % len(books)
    return books

def run_ratings(books, chunk_size=20):
    print "Gathering ratings",
    for i in xrange(0, len(books), chunk_size):
        goodreads.insert_ratings(books[i:i+chunk_size])
        sleep(0.5)
    print
    return books

def scrape(output=None):
    if output is None:
        output = DEFAULT_OUTPUT

    books = run_spider()
    books = run_ratings(books)
    json.dump(books, open(output, "w"), separators=(",", ":"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(usage=r"%(prog)s [options]" + __doc__)
    parser.add_argument("--output", "-o",
                        help="Output file for JSON data")
    args = parser.parse_args()
    scrape(args.output)
