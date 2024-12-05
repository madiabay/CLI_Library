"""System entry point."""
import sys
import json
from books.repositories import BookRepository, BookRepositoryInterface
from books.handlers import BookHandler
from user_input_data import (
    get_book_data_from_request,
    get_book_id_for_delete,
    search_books,
    get_data_for_change_book_status,
)

COMMANDS: dict = {  # all commands in command line
    1: 'Add book',
    2: 'Remove book',
    3: 'List books',
    4: 'Search books',
    5: 'Change book\'s status',
    0: 'Exit',
}


def main():
    """Command line interface."""
    book_repository: BookRepositoryInterface = BookRepository()
    book_handler = BookHandler(book_repository)

    while True:
        beautiful_commands = '\n'.join(f'{key}: {value}' for key, value in COMMANDS.items())
        command = input(beautiful_commands + '\nChoose a command: ')

        try:
            match command.capitalize():
                case '1' | 'Add book':
                    book_data = get_book_data_from_request()
                    response_dict, _ = book_handler.add_book(**book_data)
                case '2' | 'Remove book':
                    book_id = get_book_id_for_delete()
                    response_dict = book_handler.remove_book(book_id=book_id)
                case '3' | 'List books':
                    response_dict, all_books = book_handler.get_books()
                    print(json.dumps(all_books, indent=4))
                case '4' | 'Search books':
                    response_dict, search_string = book_handler.search_books(query_string=search_books())
                    print(json.dumps(search_string, indent=4))
                case '5' | 'Change book\'s status':
                    change_book_datas = get_data_for_change_book_status()
                    response_dict = book_handler.change_book_status(**change_book_datas)
                case '0' | 'Exit':
                    sys.exit(0)
                case _:
                    print('Invalid command\n')
                    continue
        except Exception as e:
            print()
            print(f'ERROR -> {e}')
            if input('Main page or Exit (M/E): ').upper() == 'M':
                print()
                continue
            else:
                print()
                break
        else:
            print()
            print(f'{response_dict['message']} HTTP-{response_dict['status_code']}')
            if input('Main page or Exit (M/E): ').upper() == 'M':
                print()
                continue
            else:
                print()
                break


if __name__ == '__main__':
    main()
