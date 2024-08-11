import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the PIL library
import sqlite3
import subprocess

# Function to set up the database for the assessment data to be stored
def setup_database():
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_code TEXT PRIMARY KEY,
            subject_name TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT,
            assessment_type TEXT,
            credits_available INTEGER,
            grade_achieved TEXT,
            credits_achieved INTEGER,
            FOREIGN KEY(subject_code) REFERENCES subjects(subject_code)
        )
    ''')

    # List of subject for the 'Subject Code' column
    subjects = [
        ("13MAT", "Mathematics"),
        ("13DDT", "Programming"),
        ("13DVV", "Spatial Design"),
        ("13PHY", "Physics")
    ]

    # List of assessments/standards for the above subjects
    assessments = [
        ("13MAT", "Trigonometry", 4, "", 4),
        ("13MAT", "Algebra", 5, "", 5),
        ("13DDT", "Programming", 6, "", 6),
        ("13DVV", "Spatial Design", 6, "", 6),
        ("13PHY", "Modern Physics", 3, "", 3),
        ("13PHY", "Electricity", 6, "", 6),
        ("13PHY", "Waves", 4, "", 4)
    ]

    c.executemany('INSERT OR IGNORE INTO subjects (subject_code, subject_name) VALUES (?, ?)', subjects)
    c.executemany('''
        INSERT OR IGNORE INTO assessments (subject_code, assessment_type, credits_available, grade_achieved, credits_achieved) 
        VALUES (?, ?, ?, ?, ?)
    ''', assessments)

    conn.commit()
    conn.close()

# Fetching subject data from the database
def fetch_subjects():
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    c.execute('SELECT subject_code, subject_name FROM subjects')
    subjects = c.fetchall()
    conn.close()
    return subjects

# Feteching standard data from the database
def fetch_assessments(subject_code):
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    c.execute('SELECT assessment_type, credits_available, grade_achieved, credits_achieved FROM assessments WHERE subject_code = ?', (subject_code,))
    assessments = c.fetchall()
    conn.close()
    return assessments

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
    ("13MAT - Trigonometry", "Internal", 4, "", 4),
    ("13MAT - Algebra", "External", 5, "", 5),
    ("13DDT - Programming", "Internal", 6, "", 6),
    ("13DVV - Spatial Design", "Internal", 6, "", 6),
    ("13PHY - Modern Physics", "Internal", 3, "", 3),
    ("13PHY - Electricity", "External", 6, "", 6),
    ("13PHY - Waves", "External", 4, "", 4),
]

# Table GUI. Instead of having a label for each header, used i to assign and index the headers in a loop
# This simplfies the code so it is easier to understand
headers = ["Subject Code", "Assessment Type", "Credits Available", "Grade Achieved", "Credits Achieved"]
for i, header in enumerate(headers):
    label = ctk.CTkLabel(table_frame, text=header)
    label.grid(row=0, column=i, padx=10, pady=5)

# Dropdown menu for subjects
subject_var = ctk.StringVar()
subject_options = [f"{code} - {name}" for code, name in subjects]
subject_menu = ctk.CTkOptionMenu(content_frame, variable=subject_var, values=subject_options, command=update_assessments)
subject_menu.pack(pady=10)

# Initialize assessment widgets list
assessment_widgets = []

# Function for when the user enters a grade for their subject/assessment
def update_assessments(event):
    # Splitting the 'subjects' to get only the subject code
    # e.g From above, 13MAT - Mathmematics = 13MAT
    selected_subject_code = subject_var.get().split(" - ")[0]
    assessments = fetch_assessments(selected_subject_code)
    # Feteching the assessment data from the database
    # then populating the GUI credit table with the data
    for widget in assessment_widgets:
        widget.destroy()
    for row, data in enumerate(assessments, start=1):
        for col, value in enumerate(data):
            if col == 2:  # Grade Achieved column
                entry = ctk.CTkEntry(table_frame)
                entry.insert(0, value)  # Insert the current value from the database
                entry.grid(row=row, column=col, padx=10, pady=5)
                grade_entries.append((entry, selected_subject_code, data[0]))  # Store entry widget, subject code, and assessment type
            else:
                label = ctk.CTkLabel(table_frame, text=str(value), font=("Arial", 12))
                label.grid(row=row, column=col, padx=10, pady=5)
                assessment_widgets.append(label)

# Same idea for the data as the headers, used emuerate() for subject standards through the list above.
for row, data in enumerate(subject_standards, start=1):
    for col, value in enumerate(data):
        label = ctk.CTkLabel(table_frame, text=str(value))
        label.grid(row=row, column=col, padx=10, pady=5)

# Function to save entered grades back to the database
def save_grades():
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    for entry, subject_code, assessment_type in grade_entries:
        grade = entry.get()
        c.execute('UPDATE assessments SET grade_achieved = ? WHERE subject_code = ? AND assessment_type = ?', (grade, subject_code, assessment_type))
    conn.commit()
    conn.close()

root.mainloop()
