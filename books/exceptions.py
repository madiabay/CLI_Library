"""All exceptions in the library system."""
from books.choices import BookStatus


class InvalidID(Exception):
    message = 'ID\'s length should be 32'

    def __str__(self) -> str:
        return self.message


class InvalidBookStatus(Exception):
    message = f'Invalid book status. All valid statuses: {[status.value for status in BookStatus]}'

    def __str__(self) -> str:
        return self.message


class InvalidYearFormat(Exception):
    message = f'Invalid year format. Please enter a valid year (e.g., 2023).'

    def __str__(self) -> str:
        return self.message


class BookAlreadyExists(Exception):
    message = 'The book already exists.'

    def __str__(self) -> str:
        return self.message
