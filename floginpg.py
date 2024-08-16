"""This file is the login page for my app, Next Steps."""
import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import subprocess
import re

# Sets default GUI color as light mode
# regardless of the user's system light/dark mode
customtkinter.set_appearance_mode("light")


def user_details_tble():
    """Creates a table in the SQL database if there isn't already.
    Asks the user to input information to store in the database.
    """

    with sqlite3.connect("users.db") as connection:
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


class LoginFront:
    """Class for the login page.

    Used variable of LoginFront becausethe components under
    this can be seen by the user.
    """

    def __init__(self, branch):
        """Function of the frontend of the login page.
        It has labels and buttons for the user to input their login details"""
        self.root = branch
        self.root.title("NextSteps Login")
        self.root.geometry("600x500")

        # Run the user_details_tble function
        user_details_tble()

        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        # Added a logo to the login page. Example on GC
        self.logo_image = Image.open("/users/nguyennguyen/desktop/NSLogo.png")
        self.logo = ctk.CTkImage(self.logo_image, size=(210, 206))
        self.logo_label = ctk.CTkLabel(self.root, image=self.logo, text="")
        self.logo_label.pack(pady=10)

        # Width and height for the frame
        # Changed from place to pack to add padding around the frame
        self.frame = ctk.CTkFrame(self.root, width=400, height=200)
        self.frame.pack(pady=20, padx=20)

        (ctk.CTkLabel(self.frame, text="Student ID", font=self.label_font).grid
                        (row=0, column=0, pady=10, padx=10))
        (ctk.CTkLabel(self.frame, text="Password", font=self.label_font).grid
                        (row=1, column=0, pady=10, padx=10))

        # Entry field for student_id
        self.student_id = ctk.CTkEntry(self.frame)
        self.student_id.grid(row=0, column=1, pady=10, padx=10)

        # Entry field for password
        self.password = ctk.CTkEntry(self.frame, show="*")
        self.password.grid(row=1, column=1, pady=10, padx=10)

        # Login and Register buttons on the login page
        ctk.CTkButton(self.frame, text="Login", command=self.login_backend, height=40, width=150,
                      font=self.button_font).grid(row=2, column=0, pady=20, padx=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_window, height=40, width=150,
                      font=self.button_font).grid(row=2, column=1, pady=20, padx=10)

    # Function of the register button
    # It runs and opens the register window through the RegisterWindow class
    def register_window(self):
        """Function of the register button
         It runs and opens the register window through the RegisterWindow class"""

        self.root.withdraw()
        register_window = ctk.CTkToplevel(self.root)
        RegisterWindow(register_window, self.root)

    # 1. User inputs correct details = User will get redirected to landing page
    # 2. User inputs incorrect details = User will get an 'incorrect' error message
    # 3. User leaves fields blank = User will get 'blank not allowed' error message
    def login_backend(self):
        """Function of the backend of the login page.
        This is where the code fetches the information from the database"""

        student_id = self.student_id.get()
        password = self.password.get()
        # Checking if the user has entered their details correctly
        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user_details WHERE student_id = ? '
                           'AND password = ?', (student_id, password))
            user = cursor.fetchone()
        # If the user details are correct, they will get redirected
        # to the landing page. Otherwise, they will get an error message
        if user:
            self.open_landing_pg(student_id)
        else:
            messagebox.showinfo("", "Incorrect Student ID or "
                                    "Password. Please try again")

    def open_landing_pg(self, student_id):
        """Function to open the landing page when the
        user enters the correct student ID and password"""

        self.root.withdraw()
        # Pass the student_id to the flandingpg.py script
        subprocess.run(["python3", "flandingpg.py", student_id])
        self.root.destroy()


class RegisterWindow:
    """Class of the registration window. Used variable
    RegisterWindow because what the user will see is the registration form"""

    def __init__(self, register_window, main_window):
        """Connects with the function of the register button
        'register_window' from the LoginFront class"""

        self.register_window = register_window
        self.main_window = main_window
        self.register_window.title("NextSteps Account Register")
        self.register_window.geometry("700x600")

        # Buttons and labels fonts
        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        # Disclaimer at the top of the registration form
        self.disclaimer_frame = ctk.CTkFrame(self.register_window)
        self.disclaimer_frame.place(relx=0.5, rely=0.05, anchor='n')

        # Label for the disclaimer to show text
        ctk.CTkLabel(self.disclaimer_frame,
                     text="Please enter the first 3 letters of your subjects e.g English = ENG, "
                          "DDT = DDT etc \n If you have less than 6 subjects, "
                          "fill the remaining ones with 'NA'",
                     font=self.label_font).pack(pady=10)

        self.form_frame = ctk.CTkFrame(self.register_window)
        self.form_frame.place(relx=0.5, rely=0.15, anchor='n')

        # Combined the user inputs into a list
        # so the code is smaller and efficient.
        # the labels for the entry fields are also in a list
        self.entries = {}
        labels = [
            "Full Name", "Year Level", "Student ID", "Password",
            "Subject Code 1", "Subject Code 2", "Subject Code 3",
            "Subject Code 4", "Subject Code 5", "Subject Code 6"
        ]

        # Give all the labels the same settings on the page.
        # So all the input fields are uniformly spaced out.
        # Added a line when the user inputs their password,
        # a '*' is shown instead of the character for privacy.
        # Added a confirm password to the list of input fields
        # without having it go to the database.
        for i, label in enumerate(labels + ["Confirm Password"]):
            (ctk.CTkLabel(self.form_frame, text=label, font=self.label_font).grid
             (row=i, column=0, pady=5, padx=10, sticky="w"))
            self.entries[label] = ctk.CTkEntry(self.form_frame,
                                               show="*" if "Password" in label else None)
            self.entries[label].grid(row=i, column=1, pady=5, padx=10)

        # Submit and cancel buttons on the register page
        ctk.CTkButton(self.register_window, text="Submit", command=self.register_backend, height=40, width=150,
                      font=self.button_font).place(relx=0.3, rely=0.9, anchor='center')
        ctk.CTkButton(self.register_window, text="Cancel", command=self.cancel_reg, height=40, width=150,
                      font=self.button_font).place(relx=0.7, rely=0.9, anchor='center')


    def register_backend(self):
        """Function of the backend of the register page.
        It handles the users registration"""

        values = {label: entry.get() for label, entry in self.entries.items()}
        # If the user does not fill out every input on the page, an error
        # message will appear asking the user to fill everything out
        if not all(values.values()):
            messagebox.showinfo("", "All fields are required")
            return

        password = values["Password"]
        confirm_password = values["Confirm Password"]

        # String boundary password validation.
        # Used len() to check for number of character in
        # password and set to 8-20 long.
        if len(password) < 8 or len(password) > 30:
            messagebox.showinfo("", "Your password must be between 8 and 20 characters.")
            return

        # Checking if the password contains at least
        # one uppercase letter and one number
        if not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            messagebox.showinfo("", "Your password must contain at "
                                    "least one uppercase letter and one number.")
            return

        # Check if passwords match
        if password != confirm_password:
            messagebox.showinfo("", "Your passwords do not match")
            return

        year_level = values["Year Level"]

        # Combine year level with each subject code and
        # capitalize the subject code
        for i in range(1, 7):
            values[f"Subject Code {i}"] = f"{values[f'Subject Code {i}'].upper()}"

        # If all the fields are filled out, the code will
        # connect with the SQL database and add the users details to
        # the database in the table created at the start
        try:
            with sqlite3.connect("users.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    '''INSERT INTO user_details (student_id, password, 
                    full_name, year_level, subject_code1, subject_code2, subject_code3, 
                    subject_code4, subject_code5, subject_code6) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (
                        values["Student ID"], values["Password"], values["Full Name"], values["Year Level"],
                        values["Subject Code 1"], values["Subject Code 2"], values["Subject Code 3"],
                        values["Subject Code 4"], values["Subject Code 5"], values["Subject Code 6"]
                    )
                )
                connection.commit()
                messagebox.showinfo("", "Registration Successful!")
                self.cancel_reg()

        # User input of username and password storing in database table.
        # Message box to show the user, system status.
        # Exceptions that the Student ID has already been registered.
        # Code checks if the username is already registered.
        # If yes, error message will appear through IntegrityError
        # and tells the user to choose a different ID.
        except sqlite3.IntegrityError:
            messagebox.showinfo("", "Student ID already exists. Please choose a different ID.")
        except Exception as e:
            messagebox.showinfo("", f"An error occurred: {e}")

    # If the user clicks the cancel button, the window will
    # be destroyed and the sign-in page will be visible again
    def cancel_reg(self):
        '''If the user clicks the cancel button, the window will
        be destroyed and the sign-in page will be visible again

        '''
        self.register_window.destroy()
        self.main_window.deiconify()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginFront(root)
    root.mainloop()

