import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS all_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    university TEXT NOT NULL,
    subject TEXT NOT NULL,
    course TEXT NOT NULL,
    description TEXT,
    rank_score INTEGER
)
''')

# Data to be inserted
courses = {
    "University of Auckland": {
        "Arts": [
            ("Bachelor of Arts", "A versatile degree with a range of subjects.", 180),
            ("Bachelor of Communications", "Focuses on media and communication.", 200)
        ],
        "Business, Commerce, and Finance": [
            ("Bachelor of Commerce", "Covers areas like finance, marketing, and management.", 220)
        ],
        "CADI": [
            ("Bachelor of Architectural Studies", "Learn the fundamentals of architectural design.", 250),
            ("Bachelor of Design", "Explore creative design in various mediums.", 210),
            ("Bachelor of Urban Planning (Hons)", "Focus on urban development and planning.", 230)
        ],
        "Engineering": [
            ("Bachelor of Engineering (Hons)", "A comprehensive degree in various engineering fields.", 270)
        ],
        "Health, Medicine, and Biomedical Science": [
            ("Bachelor of Biomedical Science (Hons)", "Focuses on advanced biomedical research.", 240),
            ("Bachelor of Health Science", "A broad introduction to health-related fields.", 200),
            ("Bachelor of Pharmacy", "Prepares students for careers in pharmacy.", 260)
        ],
        "Law": [
            ("Bachelor of Laws", "Provides a solid foundation in legal principles.", 290)
        ],
        "Technology, Maths, and Science": [
            ("Bachelor of Science", "Covers various scientific disciplines.", 210),
            ("Bachelor of Advanced Science (Hons)", "An advanced degree in scientific research.", 250)
        ],
    },
    "Auckland University of Technology": {
        "Computer Science": [
            ("Intro to Programming", "Introduction to basic programming concepts.", 180),
            ("Data Structures", "Covers data structures and algorithms.", 220),
            ("Algorithms", "In-depth study of algorithm design and analysis.", 230)
        ],
        "Design": [
            ("Classical Mechanics", "Basic principles of mechanics and motion.", 190),
            ("Quantum Physics", "Introduction to the principles of quantum mechanics.", 250),
            ("Thermodynamics", "Study of energy, heat, and work in physical systems.", 200)
        ]
    },
}

# Insert data into the table
for university, subjects in courses.items():
    for subject, course_list in subjects.items():
        for course, description, rank_score in course_list:
            cursor.execute(
                "INSERT INTO all_courses (university, subject, course, description, rank_score) VALUES (?, ?, ?, ?, ?)",
                (university, subject, course, description, rank_score)
            )

conn.commit()
conn.close()
