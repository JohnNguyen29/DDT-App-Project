import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

# Using a class for the course search page because it is a window
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

    # Function to run/redirect user to the landing page when button is clicked, this function runs
    def open_home(self):
        self.root.destroy()
        subprocess.run(["python3", "flandingpg.py"])

    # Same function as above just different window
    def open_credit_summary(self):
        self.root.destroy()
        subprocess.run(["python3", "fcreditpg.py"])

    # Creating the GUI for the page
    def create_gui(self, frame):
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(frame, text="University Course Search", font=title_font).pack(pady=20)

        # Filter frame
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(pady=20, fill="x")

        # University filter
        university_label = ctk.CTkLabel(filter_frame, text="Select University:", font=("Arial", 14))
        university_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Lists of universities in an CTkOptionMenu
        self.university_var = ctk.StringVar()
        university_options = ["University of Auckland", "Auckland University of Technology", "University of Otago"]
        university_menu = ctk.CTkOptionMenu(filter_frame, variable=self.university_var, values=university_options)
        university_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Subject filter
        subject_label = ctk.CTkLabel(filter_frame, text="Select Subject:", font=("Arial", 14))
        subject_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Lists of uni faculties/subjects in an CTkOptionMenu
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

    # Function to search courses and display dropdowns for each
    def search_courses(self):
        university = self.university_var.get()
        subject = self.subject_var.get()

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Connect to the database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT course, description, rank_score FROM all_courses WHERE university=? AND subject=?", (university, subject))
        courses = cursor.fetchall()

        conn.close()

        # Display search results
        if courses:
            for course, description, rank_score in courses:
                # Create a frame for each course to hold the dropdown
                course_frame = ctk.CTkFrame(self.results_frame)
                course_frame.pack(fill="x", pady=5)

                # Add the course name as a label
                course_label = ctk.CTkLabel(course_frame, text=course, font=("Arial", 14))
                course_label.pack(anchor="w")

                # Add a dropdown to show course details
                details_frame = ctk.CTkFrame(course_frame)
                details_frame.pack(fill="x", padx=20)

                # Course description and rank score
                description_label = ctk.CTkLabel(details_frame, text=f"Description: {description}", font=("Arial", 12))
                description_label.pack(anchor="w")

                rank_score_label = ctk.CTkLabel(details_frame, text=f"Entry Requirement: Rank Score {rank_score}", font=("Arial", 12))
                rank_score_label.pack(anchor="w")
        else:
            no_results_label = ctk.CTkLabel(self.results_frame, text="No courses found.", font=("Arial", 14))
            no_results_label.pack(pady=20)

if __name__ == "__main__":
    UniCourseSearchPage()
