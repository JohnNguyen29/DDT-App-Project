import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the PIL library
import sqlite3
import subprocess

# Defining the window
root = ctk.CTk()
root.title("NCEA Credit Summary")
root.geometry("800x600")

# Splitting the page into sections for different widgets and easier to code around
header_frame = ctk.CTkFrame(root, width=780, height=100)
header_frame.pack(pady=20)
header_frame.pack_propagate(False)

title_label = ctk.CTkLabel(header_frame, text="NCEA CREDIT SUMMARY")
title_label.pack()

# Define the main content frame
main_frame = ctk.CTkFrame(root, width=540, height=400, )
main_frame.pack(padx=20, pady=10)
main_frame.pack_propagate(False)

table_frame = ctk.CTkFrame(main_frame, width=520, height=200)
table_frame.pack(pady=20)
table_frame.pack_propagate(False)

# All subject standards with assessment type, credits avaliable
# and achieved and grade achieved
subject_standards = [
    ("13MAT - Trigonometry", "Internal", 4, "A", 4),
    ("13MAT - Algebra", "External", 5, "E", 5),
    ("13DDT - Programming", "Internal", 6, "E", 6),
    ("13DVV - Spatial Design", "Internal", 6, "M", 6),
    ("13PHY - Modern Physics", "Internal", 3, "A", 3),
    ("13PHY - Electricity", "External", 6, "M", 6),
    ("13PHY - Waves", "External", 4, "E", 4),
]

# Table GUI. Instead of having a label for each header, used i to assign and index the headers.
# This simplfies the code so it is easier to understand
headers = ["Subject Code", "Assessment Type", "Credits Available", "Grade Achieved", "Credits Achieved"]
for i, header in enumerate(headers):
    label = ctk.CTkLabel(table_frame, text=header)
    label.grid(row=0, column=i, padx=10, pady=5)

# Same idea for the data as the headers, used emuerate() for subject standards through the list above.
for row, data in enumerate(subject_standards, start=1):
    for col, value in enumerate(data):
        label = ctk.CTkLabel(table_frame, text=str(value))
        label.grid(row=row, column=col, padx=10, pady=5)

# Add Credits button for futher development of features
add_credits_button = ctk.CTkButton(main_frame, text="Add Credits", width=120)
add_credits_button.pack(pady=10)

root.mainloop()
