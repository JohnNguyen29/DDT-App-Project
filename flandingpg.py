import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        self.bottom_frame.pack(side="bottom", fill="x")

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

    # Function to create the GUI of the page.
    def create_gui(self, welcome_frame, top_frame, bottom_frame):
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(welcome_frame, text="Welcome! This is your NCEA summary...", font=title_font).pack(pady=20)


HomePage()
