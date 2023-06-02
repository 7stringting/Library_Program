# Made by Ali Al Aoraebi
# Youtube Video: https://youtu.be/KuIF-Bn0apw

import sqlite3
from datetime import datetime, timedelta


conn = sqlite3.connect('library.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS books(
    id integer primary key,
    title text unique not null,
    author text not null,
    genre text not null,
    quantity integer not null,
    availability text not null
)
''')

# cur.execute('''
# INSERT INTO books (id, title, author, genre, quantity, availability)
# VALUES (1, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 10, 'yes'),
#        (2, '1984', 'George Orwell', 'Fiction', 5, 'yes'),
#        (3, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 8, 'yes'),
#        (4, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Non-fiction', 12, 'yes'),
#        (5, 'The Autobiography of Malcolm X', 'Malcolm X', 'Biography', 0, 'no'),
#        (6, 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 3, 'yes'),
#        (7, 'Pride and Prejudice', 'Jane Austen', 'Fiction', 0, 'no'),
#        (8, 'The Hitchhiker''s Guide to the Galaxy', 'Douglas Adams', 'Science', 4, 'yes'),
#        (9, 'Born a Crime: Stories from a South African Childhood', 'Trevor Noah', 'Autobiography', 0, 'no'),
#        (10, 'The Power of Habit: Why We Do What We Do in Life and Business', 'Charles Duhigg', 'Non-fiction', 9, 'yes');
#
# ''')

# conn.commit()

# Object-Oriented Implementation
class Book:
    def __init__(self, id, title, author, genre, quantity, availability):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.quantity = quantity
        self.availability = availability

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_id(self):
        return self.id

    def set_book_id(self, id):
        self.id = id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_author(self):
        return self.author

    def set_author(self, author):
        self.author = author

    def get_genre(self):
        return self.genre

    def set_genre(self, genre):
        self.genre = genre

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_availability(self):
        return self.availability

    def set_availability(self, availability):
        self.availability = availability

# Saving to database
    def save_to_database(self):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()

        c.execute('''
        INSERT INTO books (id, title, author, genre, quantity, availability)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.id, self.title, self.author, self.genre, self.quantity, self.availability))

        conn.commit()
        conn.close()

# new_book = Book("16", "The Book", "F. Scott Fitzgerald", "Fiction", 5, True)
#
# new_book.save_to_database()
# conn.commit()

def print_menu():
    print("------------------------------")
    print("| 1. Display available books |")
    print("| 2. Search for a book       |")
    print("| 3. Rent a book             |")
    print("| 4. Exit program            |")
    print("------------------------------")


def get_menu_option():
    while True:
        user_input = input("Select menu option: ")
        if user_input == "1":
            display_books()
        elif user_input == "2":
            search_term = input("Search book by title, author or genre: ")
            search_term=search_term.lower()
            s=search_term[0].upper()
            print(s+search_term[1:len(search_term)])

            search_books(s+search_term[1:len(search_term)])
        elif user_input == "3":
            rent_books()
        elif user_input == "4":
            exit()
        else:
            print("Enter valid option!")


def search_books(search_term):
    # Search the database for books matching the search term
    cur.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre = ?",
                ('%' + search_term + '%', '%' + search_term +'%', search_term ))
    print(("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre = ?",
                ('%' + search_term + '%', '%' + search_term + '%',  search_term )))
    results = cur.fetchall()
    # Print the results
    if len(results) == 0:
        print("No books found.")
    else:
        print("Results:")
        for row in results:
            print("Title:", row[1])
            print("Author:", row[2])
            print("Genre:", row[3])
            print("Quantity:", row[4])
            print("Availability:", row[5])
            print("--------------------")

    user_input = input("Type 1 to search again, or 0 to exit: ")
    while True:
        if user_input == '1':
            search_term = input("Search book by title, author or genre: ")
            search_books(search_term)
        elif user_input == '0':
            library_program()
        else:
            print("invalid input!")


def rent_books():
    while True:
        book_ids_input = input("Enter the IDs of the books you would like to rent, separated by commas: ")
        try:
            book_ids = [int(book_id.strip()) for book_id in book_ids_input.split(",")]
        except ValueError:
            print("Invalid input! Please enter only numbers separated by commas.")
            continue

        # checks if any of the books are already rented out
        rented_out = []
        for book_id in book_ids:
            cur.execute("SELECT availability, quantity FROM books WHERE id=?", (book_id,))
            availability, quantity = cur.fetchone()
            if availability == "no":
                rented_out.append(str(book_id))
            elif quantity == 0:
                print(f"The following books are out of stock: {book_id}")
                return

        if len(rented_out) > 0:
            print(f"The following books are already rented out and cannot be rented at this time: {', '.join(rented_out)}")
            continue

        # update the quantity and availability of the books
        for book_id in book_ids:
            cur.execute("UPDATE books SET quantity=quantity-1 WHERE id=?", (book_id,))
            cur.execute("UPDATE books SET availability='no' WHERE id=? AND quantity=0", (book_id,))
            conn.commit()

        # generate and display the rental receipt
        due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        rented_books = []
        for book_id in book_ids:
            cur.execute("SELECT title, author FROM books WHERE id=?", (book_id,))
            book_title, author = cur.fetchone()
            rented_books.append(f"{book_title} by {author}")

        print("Rental Receipt:")
        print("----------------")
        print("Books rented:")
        for book in rented_books:
            print(f"- {book}")
        print(f"Due date: {due_date}")

        user_input = input("Type 1 to rent more, or 0 to exit: ")
        while True:
            if user_input == '1':
                rent_books()
            elif user_input == '0':
                library_program()
            else:
                print("Invalid input!")
                break
        break


def display_books():
    # Connect to the database
    connection = sqlite3.connect('library.db')
    cursor = conn.cursor()

    # Execute SQL query to retrieve all books
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    # Display header
    print('{:<10} {:<65} {:<20} {:<15} {:<10} {:<12}'.format('Book ID', 'Title', 'Author', 'Category', 'Quantity', 'Availability'))
    print('-' * 140)

    # Display each book and its availability
    for book in books:
        book_id, title, author, category, quantity, availability = book
        print('{:<10} {:<65} {:<20} {:<15} {:<10} {:<12}'.format(book_id, title, author, category, quantity, availability))

    # Close the database connection
    connection.close()
    print('')
    library_program()


def library_program():
    print_menu()
    get_menu_option()


library_program()

