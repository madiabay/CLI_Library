from typing import List

from books.choices import BookStatus
from books.models import Book

from books.repositories import BookRepositoryInterface
from books.exceptions import InvalidID, InvalidBookStatus, InvalidYearFormat


class BookHandler:
    """Handler for processing and validating book-related operations."""
    book_repository: BookRepositoryInterface

    def __init__(self, book_repository: BookRepositoryInterface):
        self.book_repository = book_repository

    def add_book(self, title: str, author: str, year: str) -> dict:
        """Process and validate book addition request."""
        if not year.isdigit() or len(year) != 4:
            raise InvalidYearFormat
        year = int(year)
        return self.book_repository.add_book(title=title, author=author, year=year)

    def remove_book(self, book_id: str) -> dict:
        """Process book deletion request."""
        if len(book_id) != 36:
            raise InvalidID
        return self.book_repository.delete_book(book_id=book_id)

    def search_books(self, query_string: str) -> tuple[dict, List[Book]]:
        """Process book search request."""
        if not query_string:
            raise ValueError("Search query cannot be empty")
        return self.book_repository.search_books(query_string)

    def get_books(self) -> tuple[dict, List[Book]]:
        """Retrieve all books from the repository."""
        return self.book_repository.get_books()

    def change_book_status(self, book_id: str, book_status: str):
        """Process book status change request."""
        if len(book_id) != 36:
            raise InvalidID
        if not book_status.upper() in BookStatus:
            raise InvalidBookStatus
        return self.book_repository.change_book_status(book_id=book_id, book_status=BookStatus[book_status.upper()])
