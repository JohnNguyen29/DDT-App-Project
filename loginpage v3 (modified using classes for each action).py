import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NextSteps Login")
        self.root.geometry("400x300")

        self.initialize_db()
        self.populate_db()

        tk.Label(root, text="Username").place(x=10, y=10)
        tk.Label(root, text="Password").place(x=10, y=40)

        self.e1 = tk.Entry(root)
        self.e1.place(x=140, y=10)

        self.e2 = tk.Entry(root)
        self.e2.place(x=140, y=40)
        self.e2.config(show="*")

        tk.Button(root, text="Login", command=self.login_user, height=2, width=10).place(x=10, y=100)
        tk.Button(root, text="Register", command=self.register_user, height=2, width=10).place(x=140, y=100)

    def initialize_db(self):
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

    def populate_db(self):
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

    def register_user(self):
        uname = self.e1.get()
        password = self.e2.get()

        if not uname or not password:
            messagebox.showinfo("", "Blank Not allowed")
            return

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute('INSERT INTO user_details (username, password) VALUES (?, ?)', (uname, password))
            connection.commit()
            messagebox.showinfo("", "Registration Success")
        except sqlite3.IntegrityError:
            messagebox.showinfo("", "Username already exists")
        finally:
            connection.close()

    def login_user(self):
        uname = self.e1.get()
        password = self.e2.get()

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
            self.root.destroy()
            subprocess.run(["python3", "landingpage.py"])
        else:
            messagebox.showinfo("", "Incorrect Username and Password")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
