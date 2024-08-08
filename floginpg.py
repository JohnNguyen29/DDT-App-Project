from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

# Initialize the database and create table if not exists
def initialize_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Populate the database with initial user details
def populate_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    user_details_list = [
        ("Alexsmith", "12AMAT"),
        ("Tessa McLaren", "12BHAH"),
        ("Corey Toss", "13RAAH"),
        ("Simon Solen", "12YHAU"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO user_details VALUES (?,?)", user_details_list)
    connection.commit()
    connection.close()

# Function to handle user registration
def register_user():
    uname = e1.get()
    password = e2.get()

    # Error message if user doesn't input anything
    if not uname or not password:
        messagebox.showinfo("", "Blank Not allowed")
        return

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # User input of username and password storing in database table. Message box to show the user, system status.
    # Code checks if the username is already registered. If yes, error message will appear through IntegrityError.
    try:
        cursor.execute('INSERT INTO user_details (username, password) VALUES (?, ?)', (uname, password))
        connection.commit()
        messagebox.showinfo("", "Registration Success")
    except sqlite3.IntegrityError:
        messagebox.showinfo("", "Username already exists")
    finally:
        connection.close()

# Function to handle user login. 3 main outcomes:
# 1. User inputs correct details = User will get redirected to landing page
# 2. User inputs incorrect details = User will get an 'incorrect' error message
# 3. User leaves fields blank = User will get 'blank not allowed' error message
def login_user():
    uname = e1.get()
    password = e2.get()

    if not uname or not password:
        messagebox.showinfo("", "Blank Not allowed")
        return

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM user_details WHERE username = ? AND password = ?', (uname, password))
    user = cursor.fetchone()

    connection.close()

    if user:
        messagebox.showinfo("", "Login Success")
        root.destroy()
        subprocess.run(["python3", "landingpage.py"])
    else:
        messagebox.showinfo("", "Incorrect Username and Password")

# Initialize and populate the database
initialize_db()
populate_db()

# GUI setup
root = Tk()
root.title("NextSteps Login")
root.geometry("400x300")

Label(root, text="Username").place(x=10, y=10)
Label(root, text="Password").place(x=10, y=40)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")

Button(root, text="Login", command=login_user, height=2, width=10).place(x=10, y=100)
Button(root, text="Register", command=register_user, height=2, width=10).place(x=140, y=100)

root.mainloop()
