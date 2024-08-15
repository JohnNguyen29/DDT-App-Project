import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS all_standards (
    subject_code TEXT,
    description TEXT,
    assessment_type TEXT,
    credits_avaliable INTEGER
)
''')

# Data to be inserted
all_standards = [
    ('13MAT', 'Mathematics and Statistics 3.1 - Apply the geometry of conic sections in solving problems', 'Internal', 3),
    ('13MAT', 'Mathematics and Statistics 3.3 - Apply trigonometric methods in solving problems', 'Internal', 4),
    ('13MAT', 'Mathematics and Statistics 3.5 - Apply the algebra of complex numbers in solving problems', 'External', 5),
    ('13MAT', 'Mathematics and Statistics 3.6 - Apply differentiation methods in solving problems', 'External', 6),
    ('13MAT', 'Mathematics and Statistics 3.7 - Apply integration methods in solving problems', 'External', 6),
    ('13ENG', 'English 3.1 - Respond critically to specified aspect(s) of studied written text(s), supported by evidence', 'External', 4),
    ('13ENG', 'English 3.2 - Respond critically to specified aspect(s) of studied visual or oral text(s), supported by evidence', 'External', 4),
    ('13ENG', 'English 3.3 - Respond critically to significant aspects of unfamiliar written texts through close reading, supported by evidence', 'External', 4),
    ('13ENG', 'English 3.4 - Produce a selection of fluent and coherent writing which develops, sustains, and structures ideas', 'Internal', 6),
    ('13ENG', 'English 3.7 - Respond critically to significant connections across texts, supported by evidence', 'Internal', 4),
    ('13DDT', 'Digital Technologies and Hangarau Matihiko 3.1 - Conduct a critical inquiry to propose a digital technologies outcome', 'Internal', 6),
    ('13DDT', 'Digital Technologies and Hangarau Matihiko 3.7 - Use complex programming techniques to develop a computer program', 'Internal', 6),
    ('13DDT', 'Digital Technologies and Hangarau Matihiko 3.8 - Use complex processes to develop a digital technologies outcome', 'Internal', 6),
    ('13DDT', 'Digital Technologies and Hangarau Matihiko 3.10 - Present a reflective analysis of developing a digital outcome', 'External', 3),
    ('13DVV', 'Design and Visual Communication 3.30 - Initiate design ideas through exploration', 'External', 4),
    ('13DVV', 'Design and Visual Communication 3.31 - Develop a visual presentation that exhibits a design outcome to an audience', 'Internal', 6),
    ('13DVV', 'Design and Visual Communication 3.32 - Resolve a spatial design through graphics practice', 'Internal', 6),
    ('13DVV', 'Design and Visual Communication 3.33 - Resolve a product design through graphics practice', 'Internal', 6),
    ('13PHY', 'Physics 3.1 - Carry out a practical investigation to test a physics theory relating two variables in a non-linear relationship', 'Internal', 4),
    ('13PHY', 'Physics 3.3 - Demonstrate understanding of wave systems', 'External', 4),
    ('13PHY', 'Physics 3.4 - Demonstrate understanding of mechanical systems', 'External', 6),
    ('13PHY', 'Physics 3.5 - Demonstrate understanding of Modern Physics', 'Internal', 3),
    ('13PHY', 'Physics 3.6 - Demonstrate understanding of electrical systems', 'External', 6),
    ('12MAT', 'Mathematics and Statistics 2.1 - Apply co-ordinate geometry methods in solving problems', 'Internal', 2),
    ('12MAT', 'Mathematics and Statistics 2.2 - Apply graphical methods in solving problems', 'Internal', 4),
    ('12MAT', 'Mathematics and Statistics 2.4 - Apply trigonometric relationships in solving problems', 'Internal', 3),
    ('12MAT', 'Mathematics and Statistics 2.6 - Apply algebraic methods in solving problems', 'External', 4),
    ('12MAT', 'Mathematics and Statistics 2.7 - Apply calculus methods in solving problems', 'External', 5),
    ('12MAT', 'Mathematics and Statistics 2.12 - Apply probability methods in solving problems', 'External', 4),
    ('12MAT', 'Mathematics and Statistics 2.14 - Apply systems of equations in solving problems', 'Internal', 2),
    ('12ENG', 'English 2.1 - Analyse specified aspect(s) of studied written text(s), supported by evidence', 'External', 4),
    ('12ENG', 'English 2.2 - Analyse specified aspect(s) of studied visual or oral text(s), supported by evidence', 'External', 4),
    ('12ENG', 'English 2.3 - Analyse significant aspects of unfamiliar written text(s) through close reading, supported by evidence', 'External', 4),
    ('12ENG', 'English 2.4 - Produce a selection of crafted and controlled writing', 'Internal', 6),
    ('12ENG', 'English 2.10 - Analyse aspects of visual and/or oral text(s) through close viewing and/or listening, supported by evidence', 'Internal', 3),
    ('12DDT', 'Digital Technologies 2.2 - Apply conventions to develop a design for a digital technologies outcome', 'Internal', 3),
    ('12DDT', 'Digital Technologies 2.4 - Use advanced techniques to develop a digital media outcome', 'Internal', 4),
    ('12DDT', 'Digital Technologies 2.7 - Use advanced programming techniques to develop a computer program', 'Internal', 6),
    ('12DDT', 'Digital Technologies 2.8 - Use advanced processes to develop a digital technologies outcome', 'Internal', 6),
    ('12DDT', 'Digital Technologies 2.10 - Present a summary of developing a digital outcome', 'External', 3),
    ('12DVV', 'Design and Visual Communication 2.30 - Use visual communication techniques to generate design ideas', 'External', 3),
    ('12DVV', 'Design and Visual Communication 2.33 - Use the characteristics of a design movement or era to inform own design ideas', 'Internal', 3),
    ('12DVV', 'Design and Visual Communication 2.34 - Develop a spatial design through graphics practice', 'Internal', 6),
    ('12DVV', 'Design and Visual Communication 2.35 - Develop a product design through graphics practice', 'Internal', 6),
    ('12DVV', 'Design and Visual Communication 2.36 - Use visual communication techniques to compose a presentation of a design', 'Internal', 4),
    ('12PHY', 'Physics 2.1 - Carry out a practical physics investigation that leads to a non-linear mathematical relationship', 'Internal', 4),
    ('12PHY', 'Physics 2.3 - Demonstrate understanding of waves', 'External', 4),
    ('12PHY', 'Physics 2.4 - Demonstrate understanding of mechanics', 'External', 6),
    ('12PHY', 'Physics 2.5 - Demonstrate understanding of atomic and nuclear physics', 'Internal', 3),
    ('12PHY', 'Physics 2.6 - Demonstrate understanding of electricity and electromagnetism', 'External', 6)
]

# Insert data into the table
cursor.executemany('''
INSERT INTO all_standards (subject_code, description, assessment_type, credits_avaliable)
VALUES (?, ?, ?, ?)
''', all_standards)

conn.commit()
conn.close()
