import customtkinter as ctk
import sqlite3


# Database setup
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

    # Insert sample data using INSERT OR IGNORE
    subjects = [
        ("13MAT", "Mathematics"),
        ("13DDT", "Programming"),
        ("13DVV", "Spatial Design"),
        ("13PHY", "Physics")
    ]

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

    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Fetch data from the database
def fetch_subjects():
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    c.execute('SELECT subject_code, subject_name FROM subjects')
    subjects = c.fetchall()
    conn.close()
    return subjects


def fetch_assessments(subject_code):
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    c.execute(
        'SELECT assessment_type, credits_available, grade_achieved, credits_achieved FROM assessments WHERE subject_code = ?',
        (subject_code,))
    assessments = c.fetchall()
    conn.close()
    return assessments


# Initialize the main window
app = ctk.CTk()
app.title("NCEA Credit Summary")
app.geometry("800x600")

# Setup the database and fetch subjects
setup_database()
subjects = fetch_subjects()

# Define the header frame
header_frame = ctk.CTkFrame(app, width=780, height=100, corner_radius=10)
header_frame.pack(pady=20)
header_frame.pack_propagate(False)

# Add title
title_label = ctk.CTkLabel(header_frame, text="NCEA CREDIT SUMMARY", font=("Arial", 24))
title_label.pack()

# Define the left menu frame
menu_frame = ctk.CTkFrame(app, width=200, height=400, corner_radius=10)
menu_frame.pack(side="left", padx=20, pady=10)
menu_frame.pack_propagate(False)

# Add menu items
menu_items = ["Home", "Credit Summary", "Course Search", "Help Center"]
for item in menu_items:
    btn = ctk.CTkButton(menu_frame, text=item, width=180)
    btn.pack(pady=10)

# Define the main content frame
content_frame = ctk.CTkFrame(app, width=540, height=400, corner_radius=10)
content_frame.pack(side="right", padx=20, pady=10)
content_frame.pack_propagate(False)

# Add sections
sections = [("LEVEL 1 NUMERACY", "LEVEL 1 EXCELLENCE ENDORSEMENT"),
            ("LEVEL 1 LITERACY", "LEVEL 2 EXCELLENCE ENDORSEMENT"),
            ("UE LITERACY", "LEVEL 3 EXCELLENCE ENDORSEMENT")]

for left, right in sections:
    frame = ctk.CTkFrame(content_frame, width=520, height=50, corner_radius=10)
    frame.pack(pady=10)
    frame.pack_propagate(False)

    left_label = ctk.CTkLabel(frame, text=left, font=("Arial", 14))
    left_label.pack(side="left", padx=20)

    right_label = ctk.CTkLabel(frame, text=right, font=("Arial", 14))
    right_label.pack(side="right", padx=20)

# Add the table
table_frame = ctk.CTkFrame(content_frame, width=520, height=200, corner_radius=10)
table_frame.pack(pady=20)
table_frame.pack_propagate(False)

# Table headers
headers = ["Subject Code", "Assessment Type", "Credits Available", "Grade Achieved", "Credits Achieved"]
for i, header in enumerate(headers):
    lbl = ctk.CTkLabel(table_frame, text=header, font=("Arial", 12, "bold"))
    lbl.grid(row=0, column=i, padx=10, pady=5)


# Function to update assessments in the table based on selected subject
def update_assessments(event):
    selected_subject_code = subject_var.get().split(" - ")[0]
    assessments = fetch_assessments(selected_subject_code)
    for widget in assessment_widgets:
        widget.destroy()
    for row, data in enumerate(assessments, start=1):
        for col, value in enumerate(data):
            if col == 2:  # Grade Achieved column
                entry = ctk.CTkEntry(table_frame)
                entry.insert(0, value)  # Insert the current value from the database
                entry.grid(row=row, column=col, padx=10, pady=5)
                grade_entries.append(
                    (entry, selected_subject_code, data[0]))  # Store entry widget, subject code, and assessment type
            else:
                lbl = ctk.CTkLabel(table_frame, text=str(value), font=("Arial", 12))
                lbl.grid(row=row, column=col, padx=10, pady=5)
                assessment_widgets.append(lbl)


# Dropdown menu for subjects
subject_var = ctk.StringVar()
subject_options = [f"{code} - {name}" for code, name in subjects]
subject_menu = ctk.CTkOptionMenu(content_frame, variable=subject_var, values=subject_options,
                                 command=update_assessments)
subject_menu.pack(pady=10)

# Initialize assessment widgets list
assessment_widgets = []

# Add "Add Credits" button
add_credits_button = ctk.CTkButton(content_frame, text="Add Credits", width=120)
add_credits_button.pack(pady=10)


# Define a function to save entered grades back to the database
def save_grades():
    conn = sqlite3.connect('ncea_credits.db')
    c = conn.cursor()
    for entry, subject_code, assessment_type in grade_entries:
        grade = entry.get()
        c.execute('UPDATE assessments SET grade_achieved = ? WHERE subject_code = ? AND assessment_type = ?',
                  (grade, subject_code, assessment_type))
    conn.commit()
    conn.close()
    print("Grades saved successfully")


# Add a button to save the entered grades to the database
save_grades_button = ctk.CTkButton(content_frame, text="Save Grades", command=save_grades)
save_grades_button.pack(pady=10)

app.mainloop()
