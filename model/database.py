import sqlite3
import webscrape


def make_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("CREATE TABLE IF NOT EXISTS users("
               + "id integer PRIMARY KEY,"
               + "username text,"
               + "email text,"
               + "password text);" )
    cursor.execute(command)
    command = ("CREATE TABLE IF NOT EXISTS wishlists("
              + "id integer PRIMARY KEY,"
              + "user_id integer,"
              + "book1 text DEFAULT null,"
              + "book2 text DEFAULT null,"
              + "book3 text DEFAULT null,"
              + "book4 text DEFAULT null,"
              + "book5 text DEFAULT null,"
              + "book6 text DEFAULT null,"
              + "book7 text DEFAULT null,"
              + "book8 text DEFAULT null,"
              + "book9 text DEFAULT null,"
              + "book10 text DEFAULT null,"
              + "book11 text DEFAULT null,"
              + "book12 text DEFAULT null,"
              + "book13 text DEFAULT null,"
              + "book14 text DEFAULT null,"
              + "book15 text DEFAULT null);")
    cursor.execute(command)
    conn.commit()


def register(username, email, password):
    if username_exists(username) or email_exists(email):
        return False
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO users(username, email, password)"
              + "VALUES(?, ?, ?);")
    cursor.execute(command, (username, email, password,))
    conn.commit()
    return True


# Returns tuple of booleans
# First value True if username found
# Second value True if password matches
def login(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE username=?")
    cursor.execute(command, (username,))
    row = cursor.fetchall()
    if len(row) == 0:
        return (False, False)
    if row[0][3] == password:
        return (True, True)
    return (True, False)


def username_exists(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE username=?;")
    cursor.execute(command, (username,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    return True


def email_exists(email):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM users WHERE email=?;")
    cursor.execute(command, (email,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False
    return True


# To be used if user forgets username/password
def update_user(user_id, email, username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("UPDATE users"
               + "SET email=?,"
               + "username=?,"
               + "password=?"
               + "WHERE id=?;")
    cursor.execute(command, (email, username, password, user_id,))
    conn.commit()


def get_user_id(email='', username=''):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if not username_exists(username) and not email_exists(email):
        return False
    if email != '':
        command = ("SELECT * FROM users WHERE email=?")
        cursor.execute(command, (email,))
        row = cursor.fetchall()[0]
        return row[0]
    command = ("SELECT * FROM users WHERE username=?")
    cursor.execute(command, (username,))
    row = cursor.fetchall()[0]
    return row[0]


# Returns first open space in wishlist if it exists
# Returns True if full
def wishlist_is_full(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM wishlists WHERE user_id=?;")
    cursor.execute(command, (user_id,))
    row = cursor.fetchall()[0]
    for i in range(len(row)):
        if row[i] == None:
            return i
    return True


def create_wishlist(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("INSERT INTO wishlists(user_id)"
               + "VALUES(?);")
    cursor.execute(command, (user_id,))
    conn.commit()


def insert_book(user_id, title):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    index = wishlist_is_full(user_id)
    if index is True:
        return False
    book_num = "book" + str(index-1)
    command = ("UPDATE wishlists "
               + "SET " + book_num + "=? "
               + "WHERE user_id=?")
    print(command)
    cursor.execute(command, (title, user_id,))
    conn.commit()


def get_index(user_id, title):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM wishlists WHERE user_id=?;")
    cursor.execute(command, (user_id,))
    row = cursor.fetchall()[0]
    for i in range(len(row)):
        if row[i] == title:
            return i-1
    return 16


def delete_book(user_id, title):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    index = get_index(user_id, title)
    book_num = "book" + str(index)
    print(book_num)
    command = ("UPDATE wishlists "
               + "SET " + book_num + "=null "
               + "WHERE user_id=?;")
    cursor.execute(command, (user_id,))
    conn.commit()


def get_wishlist(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    command = ("SELECT * FROM wishlists WHERE user_id=?")
    cursor.execute(command, (user_id,))
    wishlist = list(cursor.fetchall()[0])[2:]
    while None in wishlist:
        wishlist.remove(None)
    books = set()
    for book in wishlist:
        books.update(webscrape.cheapest_textbooks(book))
        books.update(webscrape.thriftbooks(book))
    return (wishlist, books)
