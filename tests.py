"""Tests."""
import unittest
import json
import os
from books.choices import BookStatus
from books.repositories import BookRepository
from books.exceptions import BookAlreadyExists


class TestBookRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test database
        cls.test_db = 'test_database.json'
        with open(cls.test_db, 'w') as f:
            json.dump([], f)
        cls.repository = BookRepository()

    @classmethod
    def tearDownClass(cls):
        # Delete test_database after all tests
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)

    def setUp(self):
        # make sure that after each test, database will be empty
        with open(self.test_db, 'w') as f:
            json.dump([], f)

    def test_add_book(self):
        result, _ = self.repository.add_book(title="Test Book", author="Author", year=2023)
        self.assertEqual(result['status_code'], 201)
        self.assertEqual(result['message'], "Book successfully added")

    def test_add_duplicate_book(self):
        self.repository.add_book(title="Duplicate Book", author="Author", year=2023)
        with self.assertRaises(BookAlreadyExists):
            self.repository.add_book(title="Duplicate Book", author="Author", year=2023)

    def test_delete_book(self):
        _, created_book = self.repository.add_book(title="Delete Book", author="Author", year=2023)
        book_id = str(created_book.id)
        result = self.repository.delete_book(book_id)
        self.assertEqual(result['status_code'], 204)

    def test_delete_nonexistent_book(self):
        with self.assertRaises(ValueError):
            self.repository.delete_book("nonexistent-id")

    def test_search_books(self):
        self.repository.add_book(title="Python Guide", author="Author1", year=2021)
        self.repository.add_book(title="Learn Python", author="Author2", year=2022)
        result, books = self.repository.search_books("Python")
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(len(books), 2)

    def test_get_books(self):
        self.repository.add_book(title="Book 1", author="Author1", year=2021)
        self.repository.add_book(title="Book 2", author="Author2", year=2022)
        result, books = self.repository.get_books()
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(len(books), 2)

    def test_change_book_status(self):
        _, created_book = self.repository.add_book(title="Change Status", author="Author", year=2023)
        book_id = str(created_book.id)
        result = self.repository.change_book_status(book_id=book_id, book_status=BookStatus.BORROWED)
        self.assertEqual(result['status_code'], 200)

    def test_change_book_status_invalid_id(self):
        with self.assertRaises(ValueError):
            self.repository.change_book_status(book_id="invalid-id", book_status=BookStatus.BORROWED)

    def override_database_file(self, test_db):
        """Override parameter DATABASE_FILE for tests."""
        self.repository.DATABASE_FILE = test_db

    def setUp(self):
        with open(self.test_db, 'w') as f:
            json.dump([], f)
        self.override_database_file(self.test_db)

if __name__ == "__main__":
    unittest.main()
