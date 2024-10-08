import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch the users details such as student ID and subjects from 'user.db'
# instead of creating a new database, all details is all in the same database
def fetch_subject_details(student_id):
    with sqlite3.connect("../users.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT year_level, subject_code1, subject_code2, subject_code3, 
                   subject_code4, subject_code5, subject_code6 
            FROM user_details WHERE student_id = ?
        ''', (student_id,))
        user_data = cursor.fetchone()

        if not user_data:
            return None

        year_level = user_data[0]
        subjects = user_data[1:]
        return year_level, subjects


# Function to fetch all assessment/standard data from all_standards.py and all_standards SQL table
def fetch_assessments(subject_code):
    with sqlite3.connect("../users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT description, assessment_type, credits_avaliable
            FROM all_standards
            WHERE subject_code = ?
        """, (subject_code,))
        assessments = cursor.fetchall()
    return assessments

def create_grades_table():
    with sqlite3.connect("../users.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                subject_code TEXT,
                assessment_description TEXT,
                grade TEXT,
                credits INTEGER
            )
        ''')
        connection.commit()

def fetch_grades_data(student_id):
    with sqlite3.connect("../users.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT grade, SUM(credits) 
            FROM grades 
            WHERE student_id = ? 
            GROUP BY grade
        ''', (student_id,))
        data = cursor.fetchall()
    return data

# Used a class for the credit summary window to make the code easier to work with
# when add more features that require other windows
class CreditSummaryWindow:
    def __init__(self, student_id):
        self.student_id = student_id
        self.root = ctk.CTk()
        self.root.title("NCEA Credit Summary")
        self.root.geometry("1440x900")

        create_grades_table()

        # Setting the appearance mode of CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Navigation frame
        nav_frame = ctk.CTkFrame(self.root, width=200)
        nav_frame.pack(side="left", fill="y")

        self.overlay_image(nav_frame)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Different pages as frames
        self.credit_summary_frame = ctk.CTkFrame(self.main_frame)
        self.credit_summary_frame.grid(row=0, column=0, sticky="nsew")

        # Navigation buttons
        buttons = [
            ("Home", None),
            ("Credit Summary", self.credit_summary_frame),  # Button to open credit summary script
            ("Course Search", None),  # Button to open course search script
            ("Help Center", None)  # Button to open help center script
        ]

        # For loop for all buttons. If clicked, the function command coded above runs.
        for button_text, frame in buttons:
            if frame:
                button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                       command=lambda f=frame: self.show_frame(f))
            elif button_text == "Credit Summary":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=self.open_credit_summary)
            elif button_text == "Course Search":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=self.open_course_search)
            elif button_text == "Help Center":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=self.open_help_center)
            else:
                button = ctk.CTkButton(nav_frame, text=button_text, width=150)
            button.pack(pady=10)

        # Fetch data from the database and see if the student ID matches for the window to open
        result = fetch_subject_details(student_id)
        if result:
            year_level, subjects = result
            self.create_gui(self.credit_summary_frame, year_level, subjects)
        else:
            messagebox.showinfo("", "Student ID not found.")
            self.root.destroy()

        self.root.mainloop()

    # Function of the logo image on the navigation bar
    def overlay_image(self, nav_frame):
        my_img = Image.open("/Users/nguyennguyen/Desktop/NSLogo.png")
        resized = my_img.resize((150, 150), Image.LANCZOS)
        new_pic = ImageTk.PhotoImage(resized)
        label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
        label.image = new_pic
        label.pack()

    # Function of opening the credit summary page (already on it)
    def open_credit_summary(self):
        self.show_frame(self.credit_summary_frame)

    # Function when button is clicked, the course search script will run
    def open_course_search(self):
        subprocess.run(["python3", "course_search.py"])

    # Function when button is clicked, the help center script will run
    def open_help_center(self):
        subprocess.run(["python3", "help_center.py"])

    # Function to show frame
    def show_frame(self, frame):
        frame.tkraise()

    # Function of all the avaliable subjects stored in a set
    def create_gui(self, frame, year_level, subjects):
        subject_details = {
            "13MAT": "NCEA Level 3 Mathematics (Calculus)",
            "13ENG": "NCEA Level 3 English",
            "13PHY": "NCEA Level 3 Physics",
            "13DDT": "NCEA Level 3 Digital Technologies",
            "13DVV": "NCEA Level 3 Design and Visual Communication"
        }

        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(frame, text="NCEA Credit Summary", font=title_font).pack(pady=20)

        self.chart_frame = ctk.CTkFrame(frame)
        self.chart_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.table_frame = ctk.CTkFrame(frame)
        self.table_frame.pack(pady=5, padx=5, fill="both", expand=True)

        ctk.CTkButton(frame, text="Show Pie Chart", command=self.show_pie_chart).pack(pady=10)

        # Table GUI. Instead of having a label for each header, used i to assign and index the headers in a loop
        # This simplfies the code so it is easier to understand
        headers = ["Subject Code", "Assessment Description", "Assessment Type", "Credits Available", "Grade Achieved"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=header, font=title_font).grid(row=0, column=col, padx=10, pady=10)

        self.grade_entries = {}  # Dictionary to store grade entries
        self.assessment_widgets = {}  # Dictionary to store assessment widgets
        self.subject_labels = []  # List to store subject labels

        # This loop takes the subject code the user inputted in the registration form
        # and combines it with the subject description from the assessment table and displays it in the table
        for row, subject_code in enumerate(subjects, start=1):
            if subject_code:
                full_subject = f"{year_level}{subject_code} - {subject_details.get(f'{year_level}{subject_code}', 'Unknown Subject')}"
                subject_label = ctk.CTkLabel(self.table_frame, text=full_subject)
                subject_label.grid(row=row, column=0, padx=5, pady=5)

                # This is binding an action to a widget. In this case when the user left clicks on the label,
                # the function runs
                self.subject_labels.append(subject_label)
                self.assessment_widgets[subject_code] = []
                subject_label.bind("<Button-1>",
                                   lambda e, sc=f"{year_level}{subject_code}", r=row: self.toggle_assessment_display(sc,
                                                                                                                     r))
    # Function to show the assessment data
    # This is for when the subject is clicked, the assessments of the subject will show in the table
    # All other subjects will hide
    def toggle_assessment_display(self, subject_code, row):
        # Hide all widgets first
        for widget in self.table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()

        for subject_label in self.subject_labels:
            subject_label.grid()

        if hasattr(self, 'last_opened') and self.last_opened == subject_code:
            # If the same subject is clicked again, it hides all other assessments
            self.last_opened = None
            return

        self.last_opened = subject_code
        # Fetch the assessments without recursion
        assessments = fetch_assessments(subject_code)
        self.assessment_widgets[subject_code] = []  # Clear existing widgets for this subject

        for a, assessment in enumerate(assessments):
            row_offset = row + a + 1

            # Gone back to the other code from v5
            # Still does the same as previous version but less code and
            # for loop w/ if statement so its easier to understand

            description_label = ctk.CTkLabel(self.table_frame, text=assessment[0])
            description_label.grid(row=row_offset, column=1, padx=5, pady=5)

            type_label = ctk.CTkLabel(self.table_frame, text=assessment[1])
            type_label.grid(row=row_offset, column=2, padx=5, pady=5)

            credits_label = ctk.CTkLabel(self.table_frame, text=assessment[2])
            credits_label.grid(row=row_offset, column=3, padx=5, pady=5)

            # "Grade Achieved" entry should be in the last column (column 4)
            grade_entry = ctk.CTkEntry(self.table_frame)
            grade_entry.grid(row=row_offset, column=4, padx=5, pady=5)
            self.grade_entries[f"{subject_code}_{a}"] = grade_entry

            # Add the "Grade Achieved" entry widget and save button
            save_button_row = row + len(assessments) + 1
            ctk.CTkButton(self.table_frame, text="Save Grades", command=self.save_grades).grid(row=save_button_row,
                                                                                               columnspan=5, pady=5)
            # Store the widgets
            self.assessment_widgets[subject_code].extend(self.table_frame.grid_slaves(row=row_offset))

    def update_pie_chart(self):
        # Clear the previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Fetch data from the 'grades' table
        with sqlite3.connect("../users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT grade, SUM(credits) 
                FROM grades 
                WHERE student_id = ? 
                GROUP BY grade
            """, (self.student_id,))
            data = cursor.fetchall()

        grades = [row[0] for row in data]
        credits = [row[1] for row in data]

        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(credits, labels=grades, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Embed the pie chart into the CustomTkinter interface
        chart = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart.get_tk_widget().pack()
        chart.draw()

    # Modify save_grades to update the chart after saving
    def save_grades(self):
        for key, entry in self.grade_entries.items():
            subject_code, index = key.split('_')
            grade = entry.get().strip().upper()
            index = int(index)

            credits_available = [a[2] for a in fetch_assessments(subject_code)][index]
            if grade == "NA":
                credits_achieved = 0
            elif grade in ["A", "M", "E"]:
                credits_achieved = credits_available
            else:
                credits_achieved = 0

            with sqlite3.connect("../users.db") as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO grades (student_id, subject_code, assessment_description, grade, credits)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.student_id, subject_code, "Assessment Description Placeholder", grade, credits_achieved))
                connection.commit()

    # Function to add the credits and save the grade in the table
    def save_grades(self):
        for key, entry in self.grade_entries.items():
            subject_code, index = key.split('_')
            grade = entry.get().strip().upper()
            index = int(index)

            # Fetch assessment details
            assessments = fetch_assessments(subject_code)
            assessment_description = assessments[index][0]  # Get description
            credits_available = assessments[index][2]  # Get available credits

            # Determine credits achieved based on grade inputted by the user
            if grade == "NA":
                credits_achieved = 0
            elif grade in ["A", "M", "E"]:
                credits_achieved = credits_available
            else:
                credits_achieved = 0

            # Save the grade and credits into the 'grades' table
            with sqlite3.connect("../users.db") as connection:
                cursor = connection.cursor()
                cursor.execute('''
                    INSERT INTO grades (student_id, subject_code, assessment_description, grade, credits)
                    VALUES (?, ?, ?, ?, ?)
                ''', (self.student_id, subject_code, assessment_description, grade, credits_achieved))

            grid_info = entry.grid_info()
            row = grid_info.get("row")
            column = grid_info.get("column")

            print(f"Replacing entry at row: {row}, column: {column} with grade: {grade}")

            entry.grid_forget()
            grade_label = ctk.CTkLabel(self.table_frame, text=grade)
            grade_label.grid(row=entry.grid_info()["row"], column=entry.grid_info()["column"], padx=5, pady=5)

        messagebox.showinfo("Success", "Grades and credits have been saved.")
        self.update_pie_chart()  # Update the pie chart after saving grades

    def show_pie_chart(self):
        data = fetch_grades_data(self.student_id)
        grades = [row[0] for row in data]
        credits = [row[1] for row in data]

        plt.figure(figsize=(2, 2))
        plt.pie(credits, labels=grades, autopct='%1.1f%%', startangle=140)
        plt.title('Credits Distribution by Grade')
        plt.show()

if __name__ == "__main__":
    # Example student ID to fetch details
    student_id = "22656"
    CreditSummaryWindow(student_id)
