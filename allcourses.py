import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the all_courses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS all_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university TEXT NOT NULL,
    subject TEXT NOT NULL,
    course TEXT NOT NULL
)
''')

# Define course data
courses = {
    "University of Auckland": {
        "Arts": ["Bachelor of Arts", "Bachelor of Communications"],
        "Business, Commerce, and Finance": ["Bachelor of Commerce"],
        "CADI": ["Bachelor of Architectural Studies", "Bachelor of Design", "Bachelor of Urban Planning (Hons)"],
        "Engineering": ["Bachelor of Engineering (Hons)"],
        "Health, Medicine, and Biomedical Science": ["Bachelor of Biomedical Science (Hons)", "Bachelor of Health Science", "Bachelor of Pharmacy"],
        "Law": ["Bachelor of Laws"],
        "Technology, Maths, and Science": ["Bachelor of Science", "Bachelor of Advanced Science (Hons)"],
    },
    "Auckland University of Technology": {
        "Computer Science": ["Intro to Programming", "Data Structures", "Algorithms"],
        "Design": ["Classical Mechanics", "Quantum Physics", "Thermodynamics"]
    },
}

# Populate the table with data
for university, subjects in courses.items():
    for subject, course_list in subjects.items():
        for course in course_list:
            cursor.execute("INSERT INTO all_courses (university, subject, course) VALUES (?, ?, ?)",
                           (university, subject, course))

# Commit changes and close the connection
conn.commit()
conn.close()
