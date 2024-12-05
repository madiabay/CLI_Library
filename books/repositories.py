import os
import json
from typing import Protocol, List

from books.models import Book
from books.choices import BookStatus
from books.exceptions import BookAlreadyExists


class BookRepositoryInterface(Protocol):
    """The Interface for BookRepository."""

    @staticmethod
    def add_book(title: str, author: str, year: int) -> dict:
        """Add a new book to the library."""
        raise NotImplementedError

    @staticmethod
    def get_books() -> tuple[dict, List[Book]]:
        """Retrieve all books from the library."""
        raise NotImplementedError

    @staticmethod
    def delete_book(book_id: str) -> dict:
        """Delete a book from the library."""
        raise NotImplementedError

    @staticmethod
    def search_books(query_string: str) -> tuple[dict, List[Book]]:
        """Search for books matching the query string."""
        raise NotImplementedError

    @staticmethod
    def change_book_status(book_id: str, book_status: BookStatus) -> dict:
        """Change the status of a book."""
        raise NotImplementedError


class BookRepository:
    """Implementation of the BookRepositoryInterface using JSON file storage."""

    @staticmethod
    def add_book(title: str, author: str, year: int) -> dict:
        if os.path.getsize('database.json') == 0:
            books = []
        else:
            with open('database.json', 'r') as file:
                books = json.load(file)

        for book in books:
            if book['title'] == title and book['author'] == author and book['year'] == year:
                raise BookAlreadyExists
        book = Book(title=title, author=author, year=year)

        books.append(
            {
                "id": str(book.id),
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "status": book.status.value,
            }
        )
        with open('database.json', 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book successfully added", 'status_code': 201}

    @staticmethod
    def delete_book(book_id: str) -> dict:
        with open('database.json', 'r') as file:
            books = json.load(file)

        original_length = len(books)
        books = [book for book in books if book.get('id') != book_id]

        if original_length == len(books):
            raise ValueError(f"Book with id {book_id} not found")

        with open('database.json', 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book with {book_id=} successfully deleted", 'status_code': 204}

    @staticmethod
    def search_books(query_string: str) -> tuple[dict, List[Book]]:
        with open('database.json', 'r') as file:
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

    @staticmethod
    def get_books() -> tuple[dict, List[Book]]:
        with open('database.json', 'r') as file:
            books = json.load(file)

        return {'message': 'All books received', 'status_code': 200}, books

    @staticmethod
    def change_book_status(book_id: str, book_status: BookStatus) -> dict:
        with open('database.json', 'r') as file:
            books = json.load(file)

        for book in books:
            if book['id'] == book_id:
                book['status'] = book_status.value
                break
        else:
            raise ValueError(f"Book with id {book_id} not found")

        with open('database.json', 'w') as file:
            json.dump(books, file, indent=4)

        return {'message': f"Book's status updated", 'status_code': 200}
