import unittest
from hamcrest import assert_that, is_

from lib.genres import Genres

class TestGenre(unittest.TestCase):
    def test_no_books_returns_nothing(self):
        books = []
        genres = Genres(books)

        assert_that(genres.section_list, is_([]))
        assert_that(genres.genre_map, is_({}))

    def test_one_book_returns_a_single_genre(self):
        books = [{"genre": "Memoirs"}]
        genres = Genres(books)

        assert_that(genres.section_list, is_(["Biography & True Stories"]))
        assert_that(genres.genre_map, is_(
            {"Biography & True Stories": [{"name": "Memoirs",
                                           "index": 3,
                                           "book_count": 1}]}))

    def test_two_books_in_the_same_genre(self):
        books = [{"genre": "Memoirs"}, {"genre": "Memoirs"}]
        genres = Genres(books)

        assert_that(genres.section_list, is_(["Biography & True Stories"]))
        assert_that(genres.genre_map, is_(
            {"Biography & True Stories": [{"name": "Memoirs",
                                           "index": 3,
                                           "book_count": 2}]}))

    def test_two_genres_in_the_same_section(self):
        books = [{"genre": "Memoirs"}, {"genre": "True stories"}]
        genres = Genres(books)

        assert_that(genres.section_list, is_(["Biography & True Stories"]))
        assert_that(genres.genre_map, is_(
            {"Biography & True Stories": [{"name": "Memoirs",
                                           "index": 3,
                                           "book_count": 1},
                                          {"name": "True stories",
                                           "index": 4,
                                           "book_count": 1}]}))

    def test_two_genres_in_the_different_sections(self):
        books = [{"genre": "History"}, {"genre": "Memoirs"}]
        genres = Genres(books)

        assert_that(genres.section_list, is_(["Biography & True Stories",
                                              "Humanities"]))
        assert_that(genres.genre_map, is_(
            {"Biography & True Stories": [{"name": "Memoirs",
                                           "index": 3,
                                           "book_count": 1}],
             "Humanities":               [{"name": "History",
                                           "index": 52,
                                           "book_count": 1}]}))

    def test_book_with_unknown_genre_is_in_unrecognised_genre(self):
        books = [{"genre": "Won't recognise this"}]
        genres = Genres(books)

        assert_that(genres.section_list, is_(["Unrecognised"]))
        assert_that(genres.genre_map, is_(
            {"Unrecognised": [{"name": "Unrecognised",
                               "index": 110,
                               "book_count": 1}]}))
