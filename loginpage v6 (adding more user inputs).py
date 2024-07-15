import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3


def connect_db():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_details (
            student_id TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            year_level TEXT NOT NULL,
            subject_code1 TEXT NOT NULL,
            subject_code2 TEXT NOT NULL,
            subject_code3 TEXT NOT NULL,
            subject_code4 TEXT NOT NULL,
            subject_code5 TEXT NOT NULL,
            subject_code6 TEXT NOT NULL
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

        tk.Label(self.frame, text="Student ID", font=self.label_font).grid(row=0, column=0, pady=10)
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
        student_id = self.e1.get()
        password = self.e2.get()

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM user_details WHERE student_id = ? AND password = ?', (student_id, password))
        user = cursor.fetchone()

        connection.close()

        if user:
            self.root.destroy()
            subprocess.run(["python3", "landingpage.py"])
        else:
            messagebox.showinfo("", "Incorrect Student ID or Password. Please try again")


class RegisterWindow:
    def __init__(self, register_window, main_window):
        self.register_window = register_window
        self.main_window = main_window
        self.register_window.title("Register")
        self.register_window.geometry("400x700")

        self.label_font = ('Helvetica', 14)
        self.button_font = ('Helvetica', 14)

        tk.Label(register_window, text="Full Name", font=self.label_font).place(x=10, y=10)
        tk.Label(register_window, text="Year Level", font=self.label_font).place(x=10, y=60)
        tk.Label(register_window, text="Student ID", font=self.label_font).place(x=10, y=110)
        tk.Label(register_window, text="Password", font=self.label_font).place(x=10, y=160)
        tk.Label(register_window, text="Subject Code 1", font=self.label_font).place(x=10, y=210)
        tk.Label(register_window, text="Subject Code 2", font=self.label_font).place(x=10, y=260)
        tk.Label(register_window, text="Subject Code 3", font=self.label_font).place(x=10, y=310)
        tk.Label(register_window, text="Subject Code 4", font=self.label_font).place(x=10, y=360)
        tk.Label(register_window, text="Subject Code 5", font=self.label_font).place(x=10, y=410)
        tk.Label(register_window, text="Subject Code 6", font=self.label_font).place(x=10, y=460)

        self.fullname_entry = tk.Entry(register_window)
        self.fullname_entry.place(x=160, y=10)

        self.yearlevel_entry = tk.Entry(register_window)
        self.yearlevel_entry.place(x=160, y=60)

        self.student_id_entry = tk.Entry(register_window)
        self.student_id_entry.place(x=160, y=110)

        self.password_entry = tk.Entry(register_window, show="#")
        self.password_entry.place(x=160, y=160)

        self.subjectcode1_entry = tk.Entry(register_window)
        self.subjectcode1_entry.place(x=160, y=210)

        self.subjectcode2_entry = tk.Entry(register_window)
        self.subjectcode2_entry.place(x=160, y=260)

        self.subjectcode3_entry = tk.Entry(register_window)
        self.subjectcode3_entry.place(x=160, y=310)

        self.subjectcode4_entry = tk.Entry(register_window)
        self.subjectcode4_entry.place(x=160, y=360)

        self.subjectcode5_entry = tk.Entry(register_window)
        self.subjectcode5_entry.place(x=160, y=410)

        self.subjectcode6_entry = tk.Entry(register_window)
        self.subjectcode6_entry.place(x=160, y=460)

        tk.Button(register_window, text="Submit", command=self.register_backend, height=2, width=10,
                  font=self.button_font).place(x=10, y=520)
        tk.Button(register_window, text="Cancel", command=self.cancel_reg, height=2, width=10,
                  font=self.button_font).place(x=160, y=520)

    def register_backend(self):
        fullname = self.fullname_entry.get()
        yearlevel = self.yearlevel_entry.get()
        student_id = self.student_id_entry.get()
        password = self.password_entry.get()
        subject_code1 = self.subjectcode1_entry.get()
        subject_code2 = self.subjectcode2_entry.get()
        subject_code3 = self.subjectcode3_entry.get()
        subject_code4 = self.subjectcode4_entry.get()
        subject_code5 = self.subjectcode5_entry.get()
        subject_code6 = self.subjectcode6_entry.get()

        if not all([fullname, yearlevel, student_id, password, subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6]):
            messagebox.showinfo("", "All fields are required")

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:
            cursor.execute(
                'INSERT INTO user_details (student_id, password, full_name, year_level, subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (student_id, password, fullname, yearlevel, subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6))
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
