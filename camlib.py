#!/usr/bin/env python
import os
import json
from flask import Flask, render_template, request

DEFAULT_JSON_PATH = "_json"
PAGE_LENGTH = 20

class CamlibFlask(Flask):
    def __init__(self, name):
        super(CamlibFlask, self).__init__(name)
        self.books = []

    def load_books(self, json_path):
        self.books = json.load(open(os.path.join(json_path, "camlib.json")))
        self.books.sort(key=lambda book: book["rating"], reverse=True)

app = CamlibFlask(__name__)

@app.route("/")
def root():
    return render_template("root.html", data=app.books[:PAGE_LENGTH], next_page=2)

@app.route("/fragment/books")
def books_fragment():
    page = int(request.args["page"])
    if page < 1:
        abort(400)

    start = (page - 1) * PAGE_LENGTH
    data = app.books[start:start + PAGE_LENGTH]
    if start + PAGE_LENGTH >= len(app.books):
        next_page = None
    else:
        next_page = page + 1

    return render_template("books_fragment.html", data=data, next_page=next_page)

@app.route("/redirect/camlib")
def camlib_redirect():
    return render_template("camlib_redirect.html", isbn=request.args["isbn"])


def setup(json_path=None):
    if json_path is None:
        json_path = DEFAULT_JSON_PATH
    app.load_books(json_path)
    print "Loaded %d books" % len(app.books)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
