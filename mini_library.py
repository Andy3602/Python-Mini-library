class Book:
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"

    def __init__(self, title, author, isbn, status=AVAILABLE):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def display_details(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Status: {self.status}")

    def to_csv_string(self):
        return f'"{self.title}","{self.author}","{self.isbn}","{self.status}"'

    @staticmethod
    def from_csv_string(csv_line):
        try:
            parts = [part.strip('"') for part in csv_line.strip().split(',')]
            if len(parts) == 4:
                return Book(title=parts[0], author=parts[1], isbn=parts[2], status=parts[3])
            else:
                return None
        except Exception as e:
            print(f"Error parsing CSV line: {e}")
            return None

class LibrarySystem:
    def __init__(self, filename="library.txt"):
        self.books = []
        self.filename = filename

    def add_book(self):
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        isbn = input("Enter ISBN: ").strip()

        if not title or not author or not isbn:
            print("Error: All fields are required.")
            return

        for book in self.books:
            if book.isbn == isbn:
                print(f"Error: Book with ISBN {isbn} already exists.")
                return

        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        print(f"\nSuccessfully added book: '{title}'")

    def search_book(self):
        query = input("Enter title or ISBN to search: ").strip().lower()
        found_books = [book for book in self.books if query in book.title.lower() or query in book.isbn.lower()]

        if not found_books:
            print(f"No books found matching '{query}'.")
        else:
            print(f"\n--- Found {len(found_books)} Book(s) ---")
            for book in found_books:
                book.display_details()
                print("-" * 20)

    def remove_book(self):
        isbn = input("Enter the ISBN of the book to remove: ").strip()
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]

        if len(self.books) < initial_count:
            print(f"Book with ISBN {isbn} removed successfully.")
        else:
            print(f"Error: Book with ISBN {isbn} not found.")

    def save_records(self):
        try:
            with open(self.filename, 'w') as f:
                for book in self.books:
                    f.write(book.to_csv_string() + '\n')
            print(f"Successfully saved {len(self.books)} records to {self.filename}.")
        except IOError as e:
            print(f"Error saving file {self.filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during save: {e}")

    def load_records(self):
        try:
            with open(self.filename, 'r') as f:
                self.books = []
                for line in f:
                    book = Book.from_csv_string(line)
                    if book:
                        self.books.append(book)
            print(f"Successfully loaded {len(self.books)} records from {self.filename}.")
        except FileNotFoundError:
            print(f"Data file '{self.filename}' not found. Starting with an empty library.")
        except IOError as e:
            print(f"Error loading file {self.filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during load: {e}")

    def display_all_books(self):
        if not self.books:
            print("The library is currently empty.")
            return

        print("\n" + "=" * 80)
        print(f"{'TITLE':<30} | {'AUTHOR':<20} | {'ISBN':<15} | {'STATUS':<10}")
        print("=" * 80)
        for book in self.books:
            print(f"{book.title:<30} | {book.author:<20} | {book.isbn:<15} | {book.status:<10}")
        print("=" * 80)

    def run_menu(self):
        print("Welcome to the Mini Library Management System!")
        self.load_records()

        while True:
            print("\n--- Main Menu ---")
            print("1. Add Book")
            print("2. Search Book")
            print("3. Remove Book")
            print("4. Display All Books")
            print("5. Save Records")
            print("6. Load Records")
            print("7. Exit")
            choice = input("Enter your choice (1-7): ").strip()

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.search_book()
            elif choice == '3':
                self.remove_book()
            elif choice == '4':
                self.display_all_books()
            elif choice == '5':
                self.save_records()
            elif choice == '6':
                self.load_records()
            elif choice == '7':
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    library = LibrarySystem()
    library.run_menu()
