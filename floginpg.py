import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sqlite3

# Function of creating a table for the users details such as username, password, name and year level.
# Changed intialize_db to connect_db to make it more easy to understand the variable
# Moved the function outside the class so it can run without being in LoginFront.
# Changed the data collected. Student ID and password to keep things simple and the subject codes of users subjects.
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

# Class for login window
class LoginFront:
    # Function of the Login GUI. What the users see when they run the app
    def __init__(self, branch):
        self.root = branch
        self.root.title("NextSteps Login")
        self.root.geometry("600x500")

        connect_db()

        self.frame = ctk.CTkFrame(branch)
        self.frame.place(relx=0.5, rely=0.5, anchor='center')

        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        ctk.CTkLabel(self.frame, text="Student ID", font=self.label_font).grid(row=0, column=0, pady=10)
        ctk.CTkLabel(self.frame, text="Password", font=self.label_font).grid(row=1, column=0, pady=10)

        self.e1 = ctk.CTkEntry(self.frame)
        self.e1.grid(row=0, column=1, pady=10, padx=10)

        self.e2 = ctk.CTkEntry(self.frame, show="*")
        self.e2.grid(row=1, column=1, pady=10, padx=10)

        ctk.CTkButton(self.frame, text="Login", command=self.login_backend, height=40, width=100, font=self.button_font).grid(
            row=2, column=0, pady=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_window, height=40, width=100,
                      font=self.button_font).grid(row=2, column=1, pady=10)

    # Function that runs and opens the register window
    def register_window(self):
        self.root.withdraw()
        register_window = ctk.CTkToplevel(self.root)
        RegisterWindow(register_window, self.root)

    # Function to handle user login. 3 main outcomes:
    # 1. User inputs correct details = User will get redirected to landing page
    # 2. User inputs incorrect details = User will get an 'incorrect' error message
    # 3. User leaves fields blank = User will get 'blank not allowed' error message
    # Changed variable to login_backend because it checks the database if login details are correct
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

# Class for the registration window because it is a different window
class RegisterWindow:
    def __init__(self, register_window, main_window):
        self.register_window = register_window
        self.main_window = main_window
        self.register_window.title("Register")
        self.register_window.geometry("400x700")

        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        ctk.CTkLabel(register_window, text="Full Name", font=self.label_font).place(x=10, y=10)
        ctk.CTkLabel(register_window, text="Year Level", font=self.label_font).place(x=10, y=60)
        ctk.CTkLabel(register_window, text="Student ID", font=self.label_font).place(x=10, y=110)
        ctk.CTkLabel(register_window, text="Password", font=self.label_font).place(x=10, y=160)
        ctk.CTkLabel(register_window, text="Subject Code 1", font=self.label_font).place(x=10, y=210)
        ctk.CTkLabel(register_window, text="Subject Code 2", font=self.label_font).place(x=10, y=260)
        ctk.CTkLabel(register_window, text="Subject Code 3", font=self.label_font).place(x=10, y=310)
        ctk.CTkLabel(register_window, text="Subject Code 4", font=self.label_font).place(x=10, y=360)
        ctk.CTkLabel(register_window, text="Subject Code 5", font=self.label_font).place(x=10, y=410)
        ctk.CTkLabel(register_window, text="Subject Code 6", font=self.label_font).place(x=10, y=460)

        self.fullname_entry = ctk.CTkEntry(register_window)
        self.fullname_entry.place(x=160, y=10)

        self.yearlevel_entry = ctk.CTkEntry(register_window)
        self.yearlevel_entry.place(x=160, y=60)

        self.student_id_entry = ctk.CTkEntry(register_window)
        self.student_id_entry.place(x=160, y=110)

        self.password_entry = ctk.CTkEntry(register_window, show="#")
        self.password_entry.place(x=160, y=160)

        self.subjectcode1_entry = ctk.CTkEntry(register_window)
        self.subjectcode1_entry.place(x=160, y=210)

        self.subjectcode2_entry = ctk.CTkEntry(register_window)
        self.subjectcode2_entry.place(x=160, y=260)

        self.subjectcode3_entry = ctk.CTkEntry(register_window)
        self.subjectcode3_entry.place(x=160, y=310)

        self.subjectcode4_entry = ctk.CTkEntry(register_window)
        self.subjectcode4_entry.place(x=160, y=360)

        self.subjectcode5_entry = ctk.CTkEntry(register_window)
        self.subjectcode5_entry.place(x=160, y=410)

        self.subjectcode6_entry = ctk.CTkEntry(register_window)
        self.subjectcode6_entry.place(x=160, y=460)

        ctk.CTkButton(register_window, text="Submit", command=self.register_backend, height=40, width=100,
                      font=self.button_font).place(x=10, y=520)
        ctk.CTkButton(register_window, text="Cancel", command=self.cancel_reg, height=40, width=100,
                      font=self.button_font).place(x=160, y=520)

    # Function to handle user registration
    # Added more fields for more user data
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
            return

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        # User input of username and password storing in database table. Message box to show the user, system status.
        # Code checks if the username is already registered. If yes, error message will appear through IntegrityError.
        try:
            cursor.execute(
                'INSERT INTO user_details (student_id, password, full_name, year_level, subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (student_id, password, fullname, yearlevel, subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6))
            connection.commit()
            messagebox.showinfo("", "Success!")
            self.cancel_reg()
        except sqlite3.IntegrityError:
            messagebox.showinfo("", "Someone thought of this before you! Make it unique!")
        finally:
            connection.close()

    # Function if the user clicks cancel, it redirects them back to the login page
    def cancel_reg(self):
        self.register_window.destroy()
        self.main_window.deiconify()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginFront(root)
    root.mainloop()
