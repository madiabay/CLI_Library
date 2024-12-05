"""
Helpers for command line interface
"""


def get_book_data_from_request() -> dict:
    print("Enter the details for the new book:")
    title = input("--Title: ").strip()
    author = input("--Author: ").strip()
    year = input("--Year (e.g., 2023): ").strip()

    return {"title": title, "author": author, "year": year}


def get_book_id_for_delete() -> str:
    print("Please enter the ID of the book you wish to remove from the library:")
    book_id = input("--Book ID: ").strip()
    return book_id


def search_books() -> str:
    print("Search by book title, author name, or publication year:")
    query = input("--Enter search text: ").strip()
    return query


def get_data_for_change_book_status() -> dict:
    print("Enter books's ID and status:")
    book_id = input("--Book ID: ").strip()
    book_status = input("--Book status (AVAILABLE or BORROWED): ").strip()
    return {
        "book_id": book_id,
        "book_status": book_status,
    }
