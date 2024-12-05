import os
import json
from typing import Protocol, List

from books.models import Book
from books.choices import BookStatus
from books.exceptions import BookAlreadyExists


class BookRepositoryInterface(Protocol):
    """The Interface for BookRepository."""

    DATABASE_FILE: str
    def add_book(self, title: str, author: str, year: int) -> tuple[dict, Book]:
        """Add a new book to the library."""
        raise NotImplementedError

    def get_books(self) -> tuple[dict, List[Book]]:
        """Retrieve all books from the library."""
        raise NotImplementedError

    def delete_book(self, book_id: str) -> dict:
        """Delete a book from the library."""
        raise NotImplementedError

    def search_books(self, query_string: str) -> tuple[dict, List[Book]]:
        """Search for books matching the query string."""
        raise NotImplementedError

    def change_book_status(self, book_id: str, book_status: BookStatus) -> dict:
        """Change the status of a book."""
        raise NotImplementedError


class BookRepository:
    """Implementation of the BookRepositoryInterface using JSON file storage."""

    DATABASE_FILE: str = 'database.json'

    def add_book(self, title: str, author: str, year: int) -> tuple[dict, Book]:
        if os.path.getsize(self.DATABASE_FILE) == 0:
            books = []
        else:
            with open(self.DATABASE_FILE, 'r') as file:
                books = json.load(file)

        for book in books:
            if book['title'] == title and book['author'] == author and book['year'] == year:
                raise BookAlreadyExists
        created_book = Book(title=title, author=author, year=year)

        books.append(
            {
                "id": str(created_book.id),
                "title": created_book.title,
                "author": created_book.author,
                "year": created_book.year,
                "status": created_book.status.value,
            }
        )
        with open(self.DATABASE_FILE, 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book successfully added", 'status_code': 201}, created_book

    def delete_book(self, book_id: str) -> dict:
        with open(self.DATABASE_FILE, 'r') as file:
            books = json.load(file)

        original_length = len(books)
        books = [book for book in books if book.get('id') != book_id]

        if original_length == len(books):
            raise ValueError(f"Book with id {book_id} not found")

        with open(self.DATABASE_FILE, 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book with {book_id=} successfully deleted", 'status_code': 204}

    def search_books(self, query_string: str) -> tuple[dict, List[Book]]:
        with open(self.DATABASE_FILE, 'r') as file:
            books = json.load(file)

        def matches_book(book: dict) -> bool:
            searchable_text = ' '.join([
                str(book.get('title', '')),
                str(book.get('author', '')),
                str(book.get('year', ''))
            ])
            return query_string.lower() in searchable_text.lower()

        return (
            {'message': 'Compatible books received', 'status_code': 200},
            [book for book in books if matches_book(book)],
        )

    def get_books(self) -> tuple[dict, List[Book]]:
        with open(self.DATABASE_FILE, 'r') as file:
            books = json.load(file)

        return {'message': 'All books received', 'status_code': 200}, books

    def change_book_status(self, book_id: str, book_status: BookStatus) -> dict:
        with open(self.DATABASE_FILE, 'r') as file:
            books = json.load(file)

        for book in books:
            if book['id'] == book_id:
                book['status'] = book_status.value
                break
        else:
            raise ValueError(f"Book with id {book_id} not found")

        with open(self.DATABASE_FILE, 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book's status updated", 'status_code': 200}
