import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

class UniCourseSearchPage:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("University Course Search")
        self.root.geometry("1440x900")

        # Setting the appearance mode of CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Navigation frame
        nav_frame = ctk.CTkFrame(self.root, width=200)
        nav_frame.pack(side="left", fill="y")

        self.overlay_image(nav_frame)

        # Navigation buttons
        buttons = [
            ("Home", self.open_home),
            ("Credit Summary", self.open_credit_summary),
            ("Course Search", None),
        ]

        for button_text, command in buttons:
            button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=command)
            button.pack(pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Create the GUI elements in the main frame
        self.create_gui(self.main_frame)

        self.root.mainloop()

    # Function to display the logo image on the navigation bar
    def overlay_image(self, nav_frame):
        my_img = Image.open("/Users/nguyennguyen/Desktop/NSLogo.png")  # Update the path
        resized = my_img.resize((200, 200), Image.LANCZOS)
        new_pic = ImageTk.PhotoImage(resized)
        label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
        label.image = new_pic
        label.pack()

    # Navigation functions
    def open_home(self):
        self.root.destroy()
        subprocess.run(["python3", "flandingpg.py"])

    def open_credit_summary(self):
        self.root.destroy()  # Close the current window
        subprocess.run(["python3", "fcreditpg.py"])

    # Create the GUI elements
    def create_gui(self, frame):
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(frame, text="University Course Search", font=title_font).pack(pady=20)

        # Filter frame
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(pady=20, fill="x")

        # University filter
        university_label = ctk.CTkLabel(filter_frame, text="Select University:", font=("Arial", 14))
        university_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.university_var = ctk.StringVar()
        university_options = ["University of Auckland", "Auckland University of Technology", "University of Otago"]
        university_menu = ctk.CTkOptionMenu(filter_frame, variable=self.university_var, values=university_options)
        university_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Subject filter
        subject_label = ctk.CTkLabel(filter_frame, text="Select Subject:", font=("Arial", 14))
        subject_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.subject_var = ctk.StringVar()
        subject_options = ["Arts", "Business, Commerce, and Finance", "CADI", "Engineering", "Health, Medicine, and Biomedical Science", "Law", "Technology, Maths, and Science"]
        subject_menu = ctk.CTkOptionMenu(filter_frame, variable=self.subject_var, values=subject_options)
        subject_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Search button
        search_button = ctk.CTkButton(filter_frame, text="Search Courses", command=self.search_courses)
        search_button.grid(row=2, columnspan=2, pady=20)

        # Results frame
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(pady=20, fill="both", expand=True)

        self.results_label = ctk.CTkLabel(self.results_frame, text="No courses found.", font=("Arial", 14))
        self.results_label.pack(pady=20)

    # Function to search courses
    def search_courses(self):
        university = self.university_var.get()
        subject = self.subject_var.get()

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Connect to the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # Query the database for matching courses
        cursor.execute("SELECT course FROM allcourses WHERE university=? AND subject=?", (university, subject))
        courses = cursor.fetchall()

        conn.close()

        # Display search results
        if courses:
            for course in courses:
                course_label = ctk.CTkLabel(self.results_frame, text=course[0], font=("Arial", 14))
                course_label.pack(pady=5)
        else:
            no_results_label = ctk.CTkLabel(self.results_frame, text="No courses found.", font=("Arial", 14))
            no_results_label.pack(pady=20)

if __name__ == "__main__":
    UniCourseSearchPage()
