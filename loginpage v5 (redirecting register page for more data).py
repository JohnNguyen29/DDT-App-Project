import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3


def connect_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            year_level TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


class LoginFront:
    def __init__(self, branch):
        self.root = branch
        self.root.title("NextSteps Login")
        self.root.geometry("600x500")

        connect_db()

        self.frame = tk.Frame(branch)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.label_font = ('Helvetica', 14)
        self.button_font = ('Helvetica', 14)

        tk.Label(self.frame, text="Username", font=self.label_font).grid(row=0, column=0, pady=10)
        tk.Label(self.frame, text="Password", font=self.label_font).grid(row=1, column=0, pady=10)

        self.e1 = tk.Entry(self.frame)
        self.e1.grid(row=0, column=1, pady=10, padx=10)

        self.e2 = tk.Entry(self.frame, show="*")
        self.e2.grid(row=1, column=1, pady=10, padx=10)

        tk.Button(self.frame, text="Login", command=self.login_backend, height=2, width=10, font=self.button_font).grid(
            row=2, column=0, pady=10)
        tk.Button(self.frame, text="Register", command=self.register_window, height=2, width=10,
                  font=self.button_font).grid(row=2, column=1, pady=10)

    def register_window(self):
        self.root.withdraw()
        register_window = tk.Toplevel(self.root)
        RegisterWindow(register_window, self.root)

    def login_backend(self):
        username = self.e1.get()
        password = self.e2.get()

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM user_details WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            self.root.destroy()
            subprocess.run(["python3", "landingpage.py"])
        else:
            messagebox.showinfo("", "Incorrect Username or Password. Please try again")


class RegisterWindow:
    def __init__(self, register_window, main_window):
        self.register_window = register_window
        self.main_window = main_window
        self.register_window.title("Register")
        self.register_window.geometry("400x400")

        self.label_font = ('Helvetica', 14)
        self.button_font = ('Helvetica', 14)

        tk.Label(register_window, text="First Name", font=self.label_font).place(x=10, y=10)
        tk.Label(register_window, text="Last Name", font=self.label_font).place(x=10, y=60)
        tk.Label(register_window, text="Year Level", font=self.label_font).place(x=10, y=110)
        tk.Label(register_window, text="Username", font=self.label_font).place(x=10, y=160)
        tk.Label(register_window, text="Password", font=self.label_font).place(x=10, y=210)

        self.firstname_entry = tk.Entry(register_window)
        self.firstname_entry.place(x=160, y=10)

        self.lastname_entry = tk.Entry(register_window)
        self.lastname_entry.place(x=160, y=60)

        self.yearlevel_entry = tk.Entry(register_window)
        self.yearlevel_entry.place(x=160, y=110)

        self.username_entry = tk.Entry(register_window)
        self.username_entry.place(x=160, y=160)

        self.password_entry = tk.Entry(register_window, show="#")
        self.password_entry.place(x=160, y=210)

        tk.Button(register_window, text="Submit", command=self.register_backend, height=2, width=10,
                  font=self.button_font).place(x=10, y=270)
        tk.Button(register_window, text="Cancel", command=self.cancel_reg, height=2, width=10,
                  font=self.button_font).place(x=160, y=270)

    def register_backend(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        yearlevel = self.yearlevel_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([firstname, lastname, yearlevel, username, password]):
            messagebox.showinfo("", "All fields are required")
            returnR

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute(
                'INSERT INTO user_details (username, password, first_name, last_name, year_level) VALUES (?, ?, ?, ?, ?)',
                (username, password, firstname, lastname, yearlevel))
            connection.commit()
            messagebox.showinfo("", "Success!")
            self.cancel_reg()
        except sqlite3.IntegrityError:
            messagebox.showinfo("", "Someone thought of this before you! Make it unique!!")
        finally:
            connection.close()

    def cancel_reg(self):
        self.register_window.destroy()
        self.main_window.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginFront(root)
    root.mainloop()
