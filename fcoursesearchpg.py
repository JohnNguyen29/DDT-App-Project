import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

class UniCourseSearchPage:
    def __init__(self, root):
        self.root = root
        self.root.title("University Course Search")
        self.root.geometry("800x600")

        # Set the appearance mode of the app
        ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(main_frame, text="University Course Search", font=("Arial", 24))
        title_label.pack(pady=10)

        # Filter frame
        filter_frame = ctk.CTkFrame(main_frame)
        filter_frame.pack(pady=20, fill="x")

        # University filter
        university_label = ctk.CTkLabel(filter_frame, text="Select University:", font=("Arial", 14))
        university_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.university_var = tk.StringVar()
        university_options = ["University of Auckland", "Auckland University of Technology", "University of Otago"]
        university_menu = ctk.CTkOptionMenu(filter_frame, variable=self.university_var, values=university_options)
        university_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Subject filter
        subject_label = ctk.CTkLabel(filter_frame, text="Select Subject:", font=("Arial", 14))
        subject_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.subject_var = tk.StringVar()
        subject_options = ["Science", "Design", "Engineering", "Law"]
        subject_menu = ctk.CTkOptionMenu(filter_frame, variable=self.subject_var, values=subject_options)
        subject_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Search button
        search_button = ctk.CTkButton(filter_frame, text="Search Courses", command=self.search_courses)
        search_button.grid(row=2, columnspan=2, pady=20)

        # Results frame
        self.results_frame = ctk.CTkFrame(main_frame)
        self.results_frame.pack(pady=20, fill="both", expand=True)

        self.results_label = ctk.CTkLabel(self.results_frame, text="No courses found.", font=("Arial", 14))
        self.results_label.pack(pady=20)

    def search_courses(self):
        university = self.university_var.get()
        subject = self.subject_var.get()

        # Simulated search results
        courses = {
            "University of Auckland": {
                "Science": ["Computer Science", "Biomedical Science", "Physics"],
                "Engineering": ["Intro to Programming", "Data Structures", "Algorithms"]
            },
            "Auckland University of Technology": {
                "Computer Science": ["Intro to Programming", "Data Structures", "Algorithms"],
                "Design": ["Classical Mechanics", "Quantum Physics", "Thermodynamics"]
            },
            # Add more universities and subjects as needed...
        }

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Display search results
        if university in courses and subject in courses[university]:
            for course in courses[university][subject]:
                course_label = ctk.CTkLabel(self.results_frame, text=course, font=("Arial", 14))
                course_label.pack(pady=5)
        else:
            no_results_label = ctk.CTkLabel(self.results_frame, text="No courses found.", font=("Arial", 14))
            no_results_label.pack(pady=20)


# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = UniCourseSearchPage(root)
    root.mainloop()