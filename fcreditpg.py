"""This file is the credit summary page for my app, Next Steps""""
import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_subject_details(student_id):
    """Function to fetch the users details such as
    student ID and subjects from 'user.db' instead of creating a new database,
    all details is all in the same database
    """
    with sqlite3.connect("users.db") as connection:
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

def fetch_assessments(subject_code):
    """Function to fetch all assessment/standard data
    from all_standards.py/all_standards SQL table
    """
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT description, assessment_type, credits_avaliable
            FROM all_standards
            WHERE subject_code = ?
        """, (subject_code,))
        assessments = cursor.fetchall()
    return assessments

def create_grades_table():
    """Function to create a table where the users progress can be tracked
    """
    with sqlite3.connect("users.db") as connection:
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
    """Function to fetch the user input data to enter
    in pie charts and progress bars
    """
    with sqlite3.connect("users.db") as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT grade, SUM(credits) 
            FROM grades 
            WHERE student_id = ? 
            GROUP BY grade
        ''', (student_id,))
        data = cursor.fetchall()
    return data

# Function to fetch only the grades and credits in 'grades' table in users.db
def fetch_grade_data():
    """Function to fetch only the grades and credits in 'grades' table in users.db
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT grade, credits FROM grades")
    grade_data = cursor.fetchall()

    conn.close()
    return grade_data


class CreditSummaryWindow:
    """Used a class for the credit summary window to make the code
    easier to work withwhen add more features that require other windows
    """
    def __init__(self, student_id):
        """Initialising attributes of the object
         Makes it easier when I will assign attributes and methods
         """
        self.student_id = student_id
        self.root = ctk.CTk()
        self.root.title("NCEA Credit Summary")
        self.root.geometry("1440x900")
        self.saved_grades = {}
        # Storing saved grades in a list

        create_grades_table()

        # Setting the appearance mode of CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Navigation frame
        nav_frame = ctk.CTkFrame(self.root, width=200)
        nav_frame.pack(side="left", fill="y")

        self.logo_image(nav_frame)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Different pages as frames
        self.credit_summary_frame = ctk.CTkFrame(self.main_frame)
        self.credit_summary_frame.grid(row=0, column=0, sticky="nsew")

        # Navigation buttons
        buttons = [
            ("Home", None),  # Set to None since it will use the `open_home` method
            ("Credit Summary", self.credit_summary_frame),
            ("Course Search", None),  # Same as Home
        ]

        # For loop that creates the buttons and the command when pressed
        # The functions below will run
        for button_text, frame in buttons:
            if frame:
                button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                       command=lambda f=frame: self.show_frame(f))
            elif button_text == "Credit Summary":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                       command=self.open_credit_summary)
            elif button_text == "Course Search":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                       command=self.open_course_search)
            elif button_text == "Home":
                button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                       command=self.open_home)
            else:
                button = ctk.CTkButton(nav_frame, text=button_text, width=150)
            button.pack(pady=10)

        # Fetch data from the database and see if the student ID
        # matches for the window to open
        result = fetch_subject_details(student_id)
        if result:
            year_level, subjects = result
            self.create_gui(self.credit_summary_frame, year_level, subjects)
        else:
            messagebox.showinfo("", "Student ID not found.")
            self.root.destroy()

        self.root.mainloop()

    # Function of the logo image on the navigation bar
    def logo_image(self, nav_frame):
        my_img = Image.open("/Users/nguyennguyen/Desktop/NSLogo.png")
        resized = my_img.resize((200, 200), Image.LANCZOS)
        new_pic = ImageTk.PhotoImage(resized)
        label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
        label.image = new_pic
        label.pack()

    # Function when button is clicked, the landing page script will run
    def open_home(self):
        self.root.destroy()  # Close the current window
        subprocess.run(["python3", "flandingpg.py", self.student_id])

    # Function when button is clicked, the course search script will run
    def open_course_search(self):
        self.root.destroy()  # Close the current window
        subprocess.run(["python3", "fcoursesearchpg.py", self.student_id])

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
            "13DVV": "NCEA Level 3 Design and Visual Communication",
            "13NA": "Extra Subject"
        }

        # Title of page and disclaimer under
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(frame, text="NCEA Credit Summary", font=title_font).pack(pady=20)

        ctk.CTkLabel(frame,
                     text="IMPORTANT: Please only enter your grades when it is FINAL. "
                          "You cannot change grades after saving.",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(pady=10)

        # Creating another frame above the table frame for the pie chart and progress bars to place
        self.chart_frame = ctk.CTkFrame(frame)
        self.chart_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.table_frame = ctk.CTkFrame(frame)
        self.table_frame.pack(pady=5, padx=5, fill="both", expand=True)

        # Button to show the progress bars, credits table, and pie chart
        # Will run update_pie_chart when clicked
        ctk.CTkButton(frame, text="Show NCEA Progress",
                      command=self.update_pie_chart).pack(pady=10)

        # Set weights for each column to distribute space
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.columnconfigure(1, weight=3)
        self.table_frame.columnconfigure(2, weight=2)
        self.table_frame.columnconfigure(3, weight=1)
        self.table_frame.columnconfigure(4, weight=2)

        # Table GUI. Instead of having a label for each header,
        # used i to assign and index the headers in a loop
        # This simplfies the code so it is easier to understand
        headers = ["Subject Code", "Assessment Description", "Assessment Type",
                   "Credits Available", "Grade Achieved"]
        for col, header in enumerate(headers):
            (ctk.CTkLabel(self.table_frame, text=header, font=title_font, width=10).grid
             (row=0, column=col, padx=10, pady=10))

        # Dictionaries and lists to store the users grade input,
        # the assessment widgets (entry label), and subject labels
        self.grade_entries = {}
        self.assessment_widgets = {}
        self.subject_labels = []

        # This loop takes the subject code the user
        # inputted in the registration form
        # and combines it with the subject description from
        # the assessment table and displays it in the table
        for row, subject_code in enumerate(subjects, start=1):
            if subject_code:
                full_subject = f"{year_level}{subject_code} - {subject_details.get
                (f'{year_level}{subject_code}', 'Unknown Subject')}"
                subject_label = ctk.CTkLabel(self.table_frame, text=full_subject)
                subject_label.grid(row=row, column=0, padx=5, pady=5)

                # This is binding an action to a widget.
                # In this case when the user left clicks on the label,
                # the function runs
                self.subject_labels.append(subject_label)
                self.assessment_widgets[subject_code] = []
                subject_label.bind("<Button-1>",
                                   lambda e, sc=f"{year_level}{subject_code}",
                                          r=row: self.toggle_assessment_display(sc,r))

    # Function to show the assessment data
    # This is for when the subject is clicked,
    # the assessments of the subject will show in the table
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
        assessments = fetch_assessments(subject_code)
        self.assessment_widgets[subject_code] = []
        # Clear existing widgets for this subject

        # For loop for to list all the assessment/standards
        # data and display them in a table
        for a, assessment in enumerate(assessments):
            row_offset = row + a + 1

            # Labels for all columns of the subject table
            description_label = ctk.CTkLabel(self.table_frame,
                                             text=assessment[0], anchor="w", wraplength=300, width=300)
            description_label.grid(row=row_offset, column=1, padx=5, pady=5)

            type_label = ctk.CTkLabel(self.table_frame, text=assessment[1], width=50)
            type_label.grid(row=row_offset, column=2, padx=5, pady=5)

            credits_label = ctk.CTkLabel(self.table_frame, text=assessment[2], width=50)
            credits_label.grid(row=row_offset, column=3, padx=5, pady=5)

            # If loop to if the a grade has already been entered
            # which will show the users input
            # Else it would display an entry field
            key = f"{subject_code}_{a}"
            if key in self.saved_grades:
                grade_label = ctk.CTkLabel(self.table_frame, text=self.saved_grades[key])
                grade_label.grid(row=row_offset, column=4, padx=5, pady=5)
            else:
                grade_entry = ctk.CTkEntry(self.table_frame, width=100)
                grade_entry.grid(row=row_offset, column=4, padx=5, pady=5)
                self.grade_entries[key] = grade_entry

            # Add the "Grade Achieved" entry widget and save button
            save_button_row = row + len(assessments) + 1
            ctk.CTkButton(self.table_frame, text="Save Grades",
                          command=self.save_grades).grid(row=save_button_row, columnspan=5, pady=5)
            # Store the widgets
            (self.assessment_widgets[subject_code].extend
             (self.table_frame.grid_slaves(row=row_offset)))

        for key, (grade_label, row, column) in self.grade_labels.items():
            grade_label.grid(row=row, column=column, padx=5, pady=5)

        """Calculating the rank score based on the grade_data
        the user has inputted in fcreditspg.py which is
        stored in the 'grades' table in 'user's db'
        """
    def calculate_scores(self, grade_data):
        excellence_credits = 0
        merit_credits = 0
        achieved_credits = 0

        # For loop to calculate each different credits for the progress bars
        for grade, credits in grade_data:
            if grade == 'E':
                excellence_credits += credits
            elif grade == 'M':
                merit_credits += credits
            elif grade == 'A':
                achieved_credits += credits

        total_credits = excellence_credits + merit_credits + achieved_credits

        # If and else loop to see and calculate the best 80 credits
        # out of E, M and A credits.
        if total_credits > 80:
            if excellence_credits >= 80:
                best_excellence_credits = 80
                best_merit_credits = 0
                best_achieved_credits = 0
            else:
                best_excellence_credits = excellence_credits
                remaining_credits = 80 - best_excellence_credits

                if (best_excellence_credits + merit_credits) >= 80:
                    best_merit_credits = remaining_credits
                    best_achieved_credits = 0
                else:
                    best_merit_credits = merit_credits
                    remaining_credits -= merit_credits
                    best_achieved_credits = min(achieved_credits, remaining_credits)
        else:
            best_excellence_credits = excellence_credits
            best_merit_credits = merit_credits
            best_achieved_credits = achieved_credits

        # Calculating rank score for each grade type of credits
        rank_score_excellence = best_excellence_credits * 4
        rank_score_merit = best_merit_credits * 3
        rank_score_achieved = best_achieved_credits * 2

        # Total rank score when all are added together
        total_rank_score = rank_score_excellence + rank_score_merit + rank_score_achieved

        return (
            excellence_credits, merit_credits, achieved_credits,
            best_excellence_credits, best_merit_credits, best_achieved_credits,
            rank_score_excellence, rank_score_merit, rank_score_achieved,
            total_rank_score
        )

    # Function to update the pie chart when the user enters a grade
    # Modified function to update the pie chart and progress bars
    def update_pie_chart(self):
        # Clear any existing widgets in chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Configure grid layout for chart_frame
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(1, weight=2)
        self.chart_frame.grid_columnconfigure(2, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)

        with sqlite3.connect("users.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT grade, SUM(credits) 
                FROM grades 
                WHERE student_id = ? 
                GROUP BY grade
            """, (self.student_id,))
            data = cursor.fetchall()

        grades = {row[0]: row[1] for row in data}

        achieved_credits = grades.get("A", 0)
        merit_credits = grades.get("M", 0)
        excellence_credits = grades.get("E", 0)

        # Calulating the credits for the table
        # Following NCEA that E credits also count as M credits and so on.
        merit_total = merit_credits + excellence_credits
        achieved_total = achieved_credits + merit_credits + excellence_credits
        total_credits = achieved_total

        # Taking the return from calculate_scores function and
        # assigning it to grade data variable
        grade_data = fetch_grade_data()
        (
            excellence_credits, merit_credits, achieved_credits,
            best_excellence_credits, best_merit_credits, best_achieved_credits,
            rank_score_excellence, rank_score_merit, rank_score_achieved,
            total_rank_score
        ) = self.calculate_scores(grade_data)

        # Left Side: Progress Bars
        progress_bar_frame = ctk.CTkFrame(self.chart_frame)
        progress_bar_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.create_progress_bar("Achieved Endorsement", achieved_total, 50,
                                 parent=progress_bar_frame)
        self.create_progress_bar("Merit Endorsement", merit_total, 50,
                                 parent=progress_bar_frame)
        self.create_progress_bar("Excellence Endorsement", excellence_credits, 50,
                                 parent=progress_bar_frame)
        self.create_progress_bar("NCEA Level Certificate", total_credits, 80,
                                 parent=progress_bar_frame)

        # Center: Rank Score Table
        rank_score_frame = ctk.CTkFrame(self.chart_frame)
        rank_score_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

        headers = ["", "Excellence Credits", "Merit Credits", "Achieved Credits"]
        data = [
            ["Number of Credits", excellence_credits, merit_credits,
             achieved_credits],
            ["Best 80 Credits", best_excellence_credits, best_merit_credits,
             best_achieved_credits],
            ["Rank Score", rank_score_excellence, rank_score_merit,
             rank_score_achieved],
            ["Total Rank Score", total_rank_score, "", ""]
        ]

        # For loop to display the rank score table headers
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(rank_score_frame, text=header, anchor="w")
            label.grid(row=0, column=i, padx=10, pady=5, sticky="w")

        # Foor loop for the values/integer of the credits
        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                label = ctk.CTkLabel(rank_score_frame, text=value, anchor="w")
                label.grid(row=row_index + 1, column=col_index, padx=10, pady=5, sticky="w")

        # Right Side: Pie Chart
        pie_chart_frame = ctk.CTkFrame(self.chart_frame)
        pie_chart_frame.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(2, 2))  # Adjust the size of the pie chart
        ax.pie([achieved_credits, merit_credits, excellence_credits],
               labels=["Achieved", "Merit", "Excellence"], autopct='%1.1f%%', startangle=90)

        chart = FigureCanvasTkAgg(fig, master=pie_chart_frame)
        chart.get_tk_widget().pack(expand=True, fill="both")

        chart.draw()

    # Modified function to create and update a progress bar with a parent frame parameter
    def create_progress_bar(self, label_text, value, max_value, parent, total=False):
        label_font = ctk.CTkFont(size=14, weight="bold") if total else None
        ctk.CTkLabel(parent, text=f"{label_text} ({value}/{max_value})", font=label_font).pack(pady=5)

        progress_bar = ctk.CTkProgressBar(parent, height=30 if total else None)
        progress_bar.set(value / max_value)  # Set the progress (value/max_value)
        progress_bar.pack(pady=5, fill="x")

    # Function to save the grades the user inputs
    # NA = 0 credits, all other grades = corrosponding credits
    # when the user clicks save, the 'grades' table will be populated with the users input
    def save_grades(self):
        student_id = self.student_id
        valid_grades = {
            "NA": "NOT ACHIEVED",
            "A": "ACHIEVED",
            "M": "MERIT",
            "E": "EXCELLENCE"
        }

        # checking to see if the grade the user has entered is one of the four grades
        for key, entry in list(self.grade_entries.items()):
            grade = entry.get().strip().upper()
            if grade not in valid_grades:
                messagebox.showerror("Invalid Grade", "Please enter a valid grade: NA, A, M, or E.")
                return

            #
            if grade:
                subject_code, assessment_index = key.rsplit("_", 1)
                assessments = fetch_assessments(subject_code)

                # Check if a grade has already been entered for this assessment
                assessment = assessments[int(assessment_index)]
                assessment_description = assessment[0]

                with sqlite3.connect("users.db") as connection:
                    cursor = connection.cursor()
                    cursor.execute('''
                        SELECT grade FROM grades 
                        WHERE student_id = ? AND subject_code = ? AND assessment_description = ?
                    ''', (student_id, subject_code, assessment_description))
                    existing_grade = cursor.fetchone()

                    #Message that indicated the a grade has already been
                    # entered in the users.db database, grades table
                    if existing_grade:
                        messagebox.showinfo("Grade Already Entered",
                                            f"Grade '{valid_grades[existing_grade[0]]}' "
                                            f"has already been entered for this assessment.")
                    else:
                        # Save the new grade if not already entered
                        cursor.execute('''
                            INSERT INTO grades (student_id, subject_code, 
                            assessment_description, grade, credits)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (student_id, subject_code, assessment_description, grade, assessment[2]))
                        connection.commit()

                        self.saved_grades[key] = grade

                        # Replace the entry field with a label showing the full grade description
                        row = entry.grid_info()["row"]
                        entry.grid_forget()

                        grade_label = ctk.CTkLabel(self.table_frame, text=valid_grades[grade])
                        grade_label.grid(row=row, column=4, padx=5, pady=5)
                        self.grade_labels[key] = (grade_label, entry.grid_info()["row"],
                                                  entry.grid_info()["column"])
                        del self.grade_entries[key]

        self.update_pie_chart()
        messagebox.showinfo("", "Grades saved successfully!")

    # Function to show the pie chart in the frame above the table frame
    # Fetches the students grades through their student ID and the grades table
    def show_pie_chart(self):
        data = fetch_grades_data(self.student_id)
        grades = [row[0] for row in data]
        credits = [row[1] for row in data]

        plt.figure(figsize=(2, 2))
        plt.pie(credits, labels=grades, autopct='%1.1f%%', startangle=140)
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        app = CreditSummaryWindow(student_id)
    else:
        print("Error: student_id argument is missing.")

