import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

# Sets default GUI color as light mode regardless of the user's system light/dark mode
customtkinter.set_appearance_mode("light")

# Creates a table in the SQL database if there isn't already. Asks the user to input information to store in the
# database.
def connect_db():
    with sqlite3.connect("../users.db") as connection:
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

# Class for the login page. Used variable of LoginFront because the components under this can be seen by the user
class LoginFront:
    # Function of the frontend of the login page. It has labels and buttons for the user to input their login details
    def __init__(self, branch):
        self.root = branch
        self.root.title("NextSteps Login")
        self.root.geometry("600x500")

        connect_db()

        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        # Add logo to the login page
        self.logo_image = Image.open("/users/nguyennguyen/desktop/NSLogo.png")
        self.logo = ctk.CTkImage(self.logo_image)
        self.logo_label = ctk.CTkLabel(self.root, image=self.logo, text="")
        self.logo_label.pack(pady=100)

        self.frame = ctk.CTkFrame(self.root, width=400, height=200)  # Width and height for the frame
        self.frame.pack(pady=20, padx=20)  # Use pack to add padding around the frame

        ctk.CTkLabel(self.frame, text="Student ID", font=self.label_font).grid(row=0, column=0, pady=10, padx=10)
        ctk.CTkLabel(self.frame, text="Password", font=self.label_font).grid(row=1, column=0, pady=10, padx=10)

        self.e1 = ctk.CTkEntry(self.frame)
        self.e1.grid(row=0, column=1, pady=10, padx=10)

        self.e2 = ctk.CTkEntry(self.frame, show="*")
        self.e2.grid(row=1, column=1, pady=10, padx=10)

        # Login and Register buttons on the login page
        ctk.CTkButton(self.frame, text="Login", command=self.login_backend, height=40, width=150,
                      font=self.button_font).grid(row=2, column=0, pady=20, padx=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_window, height=40, width=150,
                      font=self.button_font).grid(row=2, column=1, pady=20, padx=10)

    # Function of the register button
    def register_window(self):
        self.root.withdraw()
        register_window = ctk.CTkToplevel(self.root)
        RegisterWindow(register_window, self.root)

    # Function of the backend of the login page. This is where the code fetches the information from the database
    def login_backend(self):
        student_id = self.e1.get()
        password = self.e2.get()
        # Checking if the user has entered their details correctly
        with sqlite3.connect("../users.db") as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM user_details WHERE student_id = ? AND password = ?', (student_id, password))
            user = cursor.fetchone()
        # If the user details are correct, they will get redirected to the landing page. Otherwise, they will get an error message
        if user:
            subprocess.run(["python3", "landingpagetest.py"])
            self.root.destroy()
        else:
            messagebox.showinfo("", "Incorrect Student ID or Password. Please try again")


# Class of the registration window. Used variable RegisterWindow because what the user will see is the registration form
class RegisterWindow:
    # Connects with the function of the register button 'register_window' from the LoginFront class
    def __init__(self, register_window, main_window):
        self.register_window = register_window
        self.main_window = main_window
        self.register_window.title("NextSteps Account Register")
        self.register_window.geometry("700x600")
        # Buttons and labels
        self.label_font = ctk.CTkFont(size=14)
        self.button_font = ctk.CTkFont(size=14)

        # Disclaimer at the top of the registration form
        self.frame = ctk.CTkFrame(self.register_window)
        self.frame.place(relx=0.5, rely=0.05, anchor='n')

        ctk.CTkLabel(self.frame, text="Please enter the first 3 letters of your subjects e.g English = ENG, DDT = DDT etc",
                     font=self.label_font).pack(pady=10)

        self.form_frame = ctk.CTkFrame(self.register_window)
        self.form_frame.place(relx=0.5, rely=0.15, anchor='n')

        # Combined the user inputs into a list so the code is smaller and efficient.
        self.entries = {}
        labels = [
            "Full Name", "Year Level", "Student ID", "Password",
            "Subject Code 1", "Subject Code 2", "Subject Code 3",
            "Subject Code 4", "Subject Code 5", "Subject Code 6"
        ]
        # Give all the labels the same settings on the page.
        # Added a line when the user inputs their password, a '*' is shown instead of the character for privacy
        for i, label in enumerate(labels):
            ctk.CTkLabel(self.form_frame, text=label, font=self.label_font).grid(row=i, column=0, pady=5, padx=10, sticky="w")
            self.entries[label] = ctk.CTkEntry(self.form_frame, show="*" if "Password" in label else None)
            self.entries[label].grid(row=i, column=1, pady=5, padx=10)
        # Submit and cancel buttons on the register page
        ctk.CTkButton(self.register_window, text="Submit", command=self.register_backend, height=40, width=150,
                      font=self.button_font).place(relx=0.3, rely=0.85, anchor='center')
        ctk.CTkButton(self.register_window, text="Cancel", command=self.cancel_reg, height=40, width=150,
                      font=self.button_font).place(relx=0.7, rely=0.85, anchor='center')

    # Function of the backend of the register page
    def register_backend(self):
        values = {label: entry.get() for label, entry in self.entries.items()}
        # If the user does not fill out every input on the page, an error message
        # will appear asking the user to fill everything out
        if not all(values.values()):
            messagebox.showinfo("", "All fields are required")
            return

        year_level = values["Year Level"]

        # Combine year level with each subject code and capitalize the subject code
        for i in range(1, 7):
            values[f"Subject Code {i}"] = f"{year_level}{values[f'Subject Code {i}'].upper()}"

        # If all the fields are filled out, the code will connect with the SQL database
        # and add the users details to the database in the table created at the start
        try:
            with sqlite3.connect("../users.db") as connection:
                cursor = connection.cursor()
                cursor.execute(
                    '''INSERT INTO user_details (student_id, password, full_name, year_level, 
                    subject_code1, subject_code2, subject_code3, subject_code4, subject_code5, subject_code6) 
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
        # Exceptions that the Student ID has already been registered,
        # if that's the case a message will tell the user to choose a different ID.
        except sqlite3.IntegrityError:
            messagebox.showinfo("", "Student ID already exists. Please choose a different ID.")
        except Exception as e:
            messagebox.showinfo("", f"An error occurred: {e}")

    # If the user clicks the cancel button, the window will be destroyed and the sign-in page will be visible again
    def cancel_reg(self):
        self.register_window.destroy()
        self.main_window.deiconify()


if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginFront(root)
    root.mainloop()
