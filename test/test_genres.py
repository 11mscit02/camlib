import unittest
from hamcrest import assert_that, is_

from lib.genres import get_genre_tree

class TestGenre(unittest.TestCase):
    def test_no_books_returns_nothing(self):
        books = []

        tree = get_genre_tree(books)

        assert_that(tree, is_([]))

    def test_one_book_returns_a_single_genre(self):
        books = [{"genre": "Memoirs"}]

        tree = get_genre_tree(books)

        assert_that(len(tree), is_(1))
        assert_that(tree[0]["section"], is_("Biography & True Stories"))
        assert_that(tree[0]["genres"], is_([{"name": "Memoirs",
                                             "index": 3,
                                             "book_count": 1}]))

    def test_two_books_in_the_same_genre(self):
        books = [{"genre": "Memoirs"}, {"genre": "Memoirs"}]

        tree = get_genre_tree(books)

        assert_that(len(tree), is_(1))
        assert_that(tree[0]["section"], is_("Biography & True Stories"))
        assert_that(tree[0]["genres"], is_([{"name": "Memoirs",
                                             "index": 3,
                                             "book_count": 2}]))

    def test_two_genres_in_the_same_section(self):
        books = [{"genre": "Memoirs"}, {"genre": "True stories"}]

        tree = get_genre_tree(books)

        assert_that(len(tree), is_(1))
        assert_that(tree[0]["section"], is_("Biography & True Stories"))
        assert_that(tree[0]["genres"], is_([{"name": "Memoirs",
                                             "index": 3,
                                             "book_count": 1},
                                            {"name": "True stories",
                                             "index": 4,
                                             "book_count": 1}]))

    def test_two_genres_in_the_different_sections(self):
        books = [{"genre": "History"}, {"genre": "Memoirs"}]

        tree = get_genre_tree(books)

        assert_that(len(tree), is_(2))
        assert_that(tree[0]["section"], is_("Biography & True Stories"))
        assert_that(tree[0]["genres"], is_([{"name": "Memoirs",
                                             "index": 3,
                                             "book_count": 1}]))
        assert_that(tree[1]["section"], is_("Humanities"))
        assert_that(tree[1]["genres"], is_([{"name": "History",
                                             "index": 52,
                                             "book_count": 1}]))

    def test_book_with_unknown_genre_is_in_unrecognised_genre(self):
        books = [{"genre": "Won't recognise this"}]

        tree = get_genre_tree(books)

        assert_that(len(tree), is_(1))
        assert_that(tree[0]["section"], is_("Unrecognised"))
        assert_that(tree[0]["genres"], is_([{"name": "Unrecognised",
                                             "index": 110,
                                             "book_count": 1}]))
