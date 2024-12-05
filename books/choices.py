from enum import Enum


class BookStatus(Enum):
    """Statuses of a book in the library system."""
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
