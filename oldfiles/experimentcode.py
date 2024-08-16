import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3
# Class for login window
class LoginApp:
    # Function of the Login GUI. What the users see when they run the app
    def __init__(self, root):
        self.root = root
        self.root.title("NextSteps Login")
        self.root.geometry("400x300")

        self.initialize_db()

        self.frame = tk.Frame(root)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.label_font = ('Helvetica', 14)
        self.entry_font = ('Helvetica', 14)
        self.button_font = ('Helvetica', 14)

        tk.Label(self.frame, text="Username", font=self.label_font).grid(row=0, column=0, pady=10)
        tk.Label(self.frame, text="Password", font=self.label_font).grid(row=1, column=0, pady=10)

        self.e1 = tk.Entry(self.frame, font=self.entry_font)
        self.e1.grid(row=0, column=1, pady=10, padx=10)

        self.e2 = tk.Entry(self.frame, font=self.entry_font, show="*")
        self.e2.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(self.frame, text="Login", command=self.login_user, height=2, width=10, font=self.button_font).grid(
            row=2, column=0, pady=10)
        tk.Button(self.frame, text="Register", command=self.register_user, height=2, width=10,
                  font=self.button_font).grid(row=2, column=1, pady=10)

    # Function of creating a table for the users username and password
    def initialize_db(self):
        connection = sqlite3.connect("../users.db")
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_details (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()
    # Function to add the user details to the above table
    # Then add the username and password to the corrosponding user
    def populate_db(self):
        connection = sqlite3.connect("../users.db")
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
        connection = sqlite3.connect("../users.db")
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
        connection = sqlite3.connect("../users.db")
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
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)