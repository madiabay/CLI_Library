"""
Book Models
"""
import uuid
from books.choices import BookStatus


class Book:
    """Represents a book entity in the library system."""
    def __init__(self, title: str, author: str, year: int, status: BookStatus = BookStatus.AVAILABLE) -> None:
        self.id = uuid.uuid4()
        self.title = title
        self.author = author
        self.year = year
        self.status = status
