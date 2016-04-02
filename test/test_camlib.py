import unittest
import json
from hamcrest import assert_that, is_

from camlib import app

TEST_BOOKS = [{"title": "First Book",
               "genre": "True stories",
               "rating": 3},
              {"title": "Second Book",
               "genre": "History",
               "rating": 4},
              {"title": "Third Book",
               "genre": "History",
               "rating": 3.5},
              {"title": "Fourth Book",
               "genre": "Philosophy",
               "rating": 1}]

class TestCamlib(unittest.TestCase):
    def TearDown(self):
        app.reset()

    def test_no_books(self):
        app.load_data({"books": []})

        assert_that(app.books, is_([]))

    def test_books_are_sorted_by_rating(self):
        app.load_data({"books": TEST_BOOKS})

        book_titles = [book["title"] for book in app.books]
        assert_that(book_titles, is_(["Second Book", "Third Book",
                                      "First Book", "Fourth Book"]))

    def test_genre_tree_is_generated(self):
        app.load_data({"books": TEST_BOOKS})

        expected = [{'section': 'Biography & True Stories',
                     'genres': [{'index': 4,
                                 'name': 'True stories',
                                 'book_count': 1}]},
                    {'section': 'Humanities',
                     'genres': [{'index': 52,
                                 'name': 'History',
                                 'book_count': 2},
                                 {'index': 54,
                                  'name': 'Philosophy',
                                  'book_count': 1}]}]
        assert_that(app.genre_tree, is_(expected))

    def test_books_can_be_filtered_by_genre(self):
        app.load_data({"books": TEST_BOOKS})

        books = app.filter_books([52, 54])

        book_titles = [book["title"] for book in books]
        assert_that(book_titles, is_(["Second Book", "Third Book", "Fourth Book"]))
