import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Using a class for the home/landing page because it is its own window
class HomePage:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("NextSteps Home Page")
        self.root.geometry("1440x900")

        # Appearance mode of CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Navigation frame
        nav_frame = ctk.CTkFrame(self.root, width=200)
        nav_frame.pack(side="left", fill="y")

        self.overlay_image(nav_frame)

        # Navigation buttons
        buttons = [
            ("Home", None),
            ("Credit Summary", self.open_credit_summary),
            ("Course Search", self.open_course_search),
        ]

        for button_text, command in buttons:
            button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=command)
            button.pack(pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Welcome frame at the top
        self.welcome_frame = ctk.CTkFrame(self.main_frame, height=100)
        self.welcome_frame.pack(side="top", fill="x")

        # Top frame
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(side="top", fill="both", pady=10)

        # Bottom frame
        self.bottom_frame = ctk.CTkFrame(self.main_frame, height=200)
        self.bottom_frame.pack(fill="x")

        # Create the GUI elements in the frames
        self.create_gui(self.welcome_frame, self.top_frame, self.bottom_frame)
        self.root.mainloop()

    # Function to display the logo image on the navigation bar
    def overlay_image(self, nav_frame):
        my_img = Image.open("/Users/nguyennguyen/Desktop/NSLogo.png")  # Update the path
        resized = my_img.resize((200, 200), Image.LANCZOS)
        new_pic = ImageTk.PhotoImage(resized)
        label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
        label.image = new_pic
        label.pack()

    # Function to run/redirect user to the landing page when button is clicked
    def open_course_search(self):
        self.root.destroy()
        subprocess.run(["python3", "fcoursesearchpg.py"])

    # Function to redirect to the credit summary page
    def open_credit_summary(self):
        self.root.destroy()
        subprocess.run(["python3", "fcreditpg.py"])

    # Function to create the GUI
    def create_gui(self, welcome_frame, top_frame, bottom_frame):
        # Welcome message in the Welcome frame
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(welcome_frame, text="Welcome! This is your NCEA summary...", font=title_font).pack(pady=20)

        # Bottom frame content
        self.display_bookmarked_courses(bottom_frame)

    # Function to display bookmarked courses in the bottom frame
    def display_bookmarked_courses(self, frame):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT course, university, subject FROM bookmarks")
        bookmarks = cursor.fetchall()

        conn.close()

        if bookmarks:
            bookmark_label = ctk.CTkLabel(frame, text="Bookmarked Courses", font=("Arial", 16, "bold"))
            bookmark_label.pack(pady=10)

            for course, university, subject in bookmarks:
                bookmark_frame = ctk.CTkFrame(frame)
                bookmark_frame.pack(fill="x", pady=5)

                course_label = ctk.CTkLabel(bookmark_frame, text=course, font=("Arial", 14))
                course_label.pack(side="left")

                remove_button = ctk.CTkButton(bookmark_frame, text="Remove", width=100,
                                              command=lambda c=course: self.remove_bookmark(c))
                remove_button.pack(side="right")
        else:
            no_bookmarks_label = ctk.CTkLabel(frame, text="No bookmarked courses.", font=("Arial", 14))
            no_bookmarks_label.pack(pady=20)

    # Function to remove a bookmark
    def remove_bookmark(self, course):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bookmarks WHERE course=?", (course,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Bookmark Removed", f"Course '{course}' has been removed from bookmarks.")
        self.display_bookmarked_courses(self.bottom_frame)  # Refresh the bookmark list

if __name__ == "__main__":
    HomePage()
