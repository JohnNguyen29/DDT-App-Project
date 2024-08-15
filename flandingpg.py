import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Using a class for the home/landing page because it is its own window
# Taking inspiration from all the other GUI layouts
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
    def open_course_search(self):
        self.root.destroy()
        subprocess.run(["python3", "fcoursesearchpg.py"])

    # Same function as above just different window
    def open_credit_summary(self):
        self.root.destroy()
        subprocess.run(["python3", "fcreditpg.py"])

    def create_gui(self, frame):
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(frame, text="Welcome! This is your NCEA summary...", font=title_font).pack(pady=20)

        # Filter frame
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(pady=20, fill="x")

HomePage()
