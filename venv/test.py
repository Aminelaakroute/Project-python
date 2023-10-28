
class Book:
    def __init__(self, title, author, ISBN, is_available):
        self.Title = title
        self.Author = author
        self.ISBN = ISBN
        self.is_available = is_available

    def Display_info(self):
        return [self.Title, self.Author, self.ISBN, self.is_available]

class Library:
    def __init__(self, database_path):
        self.books = []
        self.database_path = database_path
        self.load_books_from_database()

    def load_books_from_database(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        books_data = cursor.fetchall()
        connection.close()

        for book_data in books_data:
            title, author, ISBN, is_available = book_data
            book = Book(title, author, ISBN, is_available)
            self.books.append(book)

    def show_available_books(self):
        available_books = [book for book in self.books if book.is_available]
        return available_books

    def show_borrowed_books(self):
        borrowed_books = [book for book in self.books if not book.is_available]
        return borrowed_books

    def add_book(self, book):
        self.books.append(book)
        self.save_book_to_database(book)

    def save_book_to_database(self, book):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (title, author, ISBN, is_available) VALUES (?, ?, ?, ?)",
                       (book.Title, book.Author, book.ISBN, book.is_available))
        connection.commit()
        connection.close()

    def borrow_book(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN and book.is_available:
                book.is_available = False
                self.update_book_in_database(book)
                return f"Book '{book.Title}' borrowed successfully."
        return "Book not available or ISBN not found."

    def return_book(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN and not book.is_available:
                book.is_available = True
                self.update_book_in_database(book)
                return f"Book '{book.Title}' returned successfully."
        return "Book not borrowed or ISBN not found."

    def update_book_in_database(self, book):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET is_available = ? WHERE ISBN = ?", (book.is_available, book.ISBN))
        connection.commit()
        connection.close()

class Client:
    def __init__(self, name, user_id):
        self.Name = name
        self.User_id = user_id
        self.BooksBorrowed = []

    def Display_User_info(self):
        user_info = f"User Name : {self.Name}\nUser ID   : {self.User_id}\nBooks Borrowed : "
        for book in self.BooksBorrowed:
            user_info += f"\n - {book.Display_info()[0]} by {book.Display_info()[1]}"
        return user_info

    def Borrow_book(self, book):
        if book.is_available:
            self.BooksBorrowed.append(book)
            book.is_available = False
            return f"{self.Name} borrowed the book: {book.Display_info()[0]} by {book.Display_info()[1]}"
        else:
            return f"{self.Name} cannot borrow the book {book.Display_info()[0]} by {book.Display_info()[1]} as it is not available."

    def return_book(self, book):
        if book in self.BooksBorrowed:
            self.BooksBorrowed.remove(book)
            book.is_available = True
            return f"{self.Name} returned the book: {book.Display_info()[0]} by {book.Display_info()[1]}"
        else:
            return f"{self.Name} did not borrow the book: {book.Display_info()[0]} by {book.Display_info()[1]}"

class LibraryManagementSystem:
    def __init__(self, database_path):
        self.library = Library(database_path)
        self.users = []

    def display_available_books(self):
        return self.library.show_available_books()

    def display_borrowed_books(self):
        return self.library.show_borrowed_books()

    def display_user_details(self):
        user_details = []
        for user in self.users:
            user_details.append(user.Display_User_info())
        return user_details

    def simulate_borrow_and_return(self, user_index, book_index):
        if 0 <= user_index < len(self.users) and 0 <= book_index < len(self.library.books):
            user = self.users[user_index]
            book = self.library.books[book_index]

            if book.is_available:
                return user.Borrow_book(book)
            else:
                return user.return_book(book)
        else:
            return "Invalid user or book index."

class LibraryManagementApp(QMainWindow):
    def __init__(self, database_path):
        super(LibraryManagementApp, self).__init__()

        self.library_system = LibraryManagementSystem(database_path)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)

        self.available_books_button = QPushButton("Show Available Books")
        self.available_books_button.clicked.connect(self.display_available_books)

        self.borrowed_books_button = QPushButton("Show Borrowed Books")
        self.borrowed_books_button.clicked.connect(self.display_borrowed_books)

        self.user_details_button = QPushButton("Show User Details")
        self.user_details_button.clicked.connect(self.display_user_details)

        self.simulate_button = QPushButton("Simulate Borrow and Return")
        self.simulate_button.clicked.connect(self.simulate_borrow_and_return)

        self.result_label = QLabel()

        self.central_layout.addWidget(self.available_books_button)
        self.central_layout.addWidget(self.borrowed_books_button)
        self.central_layout.addWidget(self.user_details_button)
        self.central_layout.addWidget(self.simulate_button)
        self.central_layout.addWidget(self.result_label)

        self.setCentralWidget(self.central_widget)

    def display_available_books(self):
        self.result_label.setText("")
        available_books = self.library_system.display_available_books()
        self.show_books_table(available_books)

    def display_borrowed_books(self):
        self.result_label.setText("")
        borrowed_books = self.library_system.display_borrowed_books()
        self.show_books_table(borrowed_books)

    def display_user_details(self):
        self.result_label.setText("")
        user_details = self.library_system.display_user_details()
        self.show_user_details_table(user_details)

    def simulate_borrow_and_return(self):
        self.result_label.setText("Simulation Result:")
        user_index = 0  # Replace with the actual user index
        book_index = 0  # Replace with the actual book index
        result = self.library_system.simulate_borrow_and_return(user_index, book_index)
        self
