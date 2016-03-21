import sys
import requests

REVIEW_URL = "http://www.goodreads.com/book/review_counts.json"

def insert_ratings(books):
    print "\b.",
    sys.stdout.flush()

    isbn_str = ",".join([book["isbn"] for book in books])
    result = {}
    for book in requests.get(REVIEW_URL + "?isbns=" + isbn_str).json()["books"]:
        result[book["isbn13"]] = book["average_rating"]

    for i, book in enumerate(books):
        isbn = book["isbn"]
        if isbn in result:
            books[i]["rating"] = result[isbn]
        else:
            books[i]["rating"] = 0

    return books
