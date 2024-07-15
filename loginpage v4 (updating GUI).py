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

        tk.Button(self.frame, text="Login", command=self.login, height=2, width=10, font=self.button_font).grid(
            row=2, column=0, pady=10)
        tk.Button(self.frame, text="Register", command=self.register, height=2, width=10,
                  font=self.button_font).grid(row=2, column=1, pady=10)

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

    def register(self):
        username = self.e1.get()
        password = self.e2.get()

        if not username or not password:
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

    def login(self):
        username = self.e1.get()
        password = self.e2.get()

        if not username or not password:
            messagebox.showinfo("", "Blank Not allowed")
            return

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM user_details WHERE username = ? AND password = ?', (username, password))
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
