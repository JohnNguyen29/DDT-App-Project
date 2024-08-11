import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess

# Function to fetch the users details such as student ID and subjects from 'user.db'
# instead of creating a new database, all details is all in the same database
def fetch_subject_details(student_id):
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


class CreditSummaryWindow:
    def __init__(self, student_id):
        self.student_id = student_id
        self.root = ctk.CTk()
        self.root.title("NCEA Credit Summary")
        self.root.geometry("1440x900")

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
                button = ctk.CTkButton(nav_frame, text=button_text, width=150)  # Default case
            button.pack(pady=10)

        # Fetch data from the database
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
        resized = my_img.resize((200, 200), Image.LANCZOS)
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

        table_frame = ctk.CTkFrame(frame)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Table GUI. Instead of having a label for each header, used i to assign and index the headers in a loop
        # This simplfies the code so it is easier to understand
        headers = ["Subject Code", "Assessment Type", "Credits Available", "Grade Achieved", "Credits Achieved"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=title_font).grid(row=0, column=col, padx=10, pady=10)

        # List of assessments/standards for the above subjects in a set and lists
        self.assessments = {
            "13MAT": [
                ["Algebra", 4, "", 0],
                ["Calculus", 5, "", 0]
            ],
            "13ENG": [
                ["Essay", 6, "", 0],
                ["Research", 3, "", 0]
            ],
            "13PHY": [
                ["Mechanics", 6, "", 0],
                ["Electricity", 4, "", 0]
            ]
        }

        self.grade_entries = {}  # Dictionary to store grade entries

        # This loop takes the subject code the user inputted in the registration form
        # and combines it with the subject description from the assessment table and displays it in the table
        for row, subject_code in enumerate(subjects, start=1):
            full_subject = f"{year_level}{subject_code} - {subject_details.get(f'{year_level}{subject_code}', 'Unknown Subject')}"
            subject_label = ctk.CTkLabel(table_frame, text=full_subject)
            subject_label.grid(row=row, column=0, padx=10, pady=10)

            # This is binding an action to a widget. In this case when the user left clicks on the label,
            # the function runs
            subject_label.bind("<Button-1>",
                               lambda e, sc=f"{year_level}{subject_code}", r=row: self.toggle_assessment_display(sc, r,
                                                                                                                 table_frame,
                                                                                                                 self.assessments))

    # Function to show the assessment data
    # This is for when the subject is clicked, the assessments of the subject will show in the table
    # All other subjects will hide
    def toggle_assessment_display(self, subject_code, row, table_frame, assessments):
        for widget in table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > row:
                widget.grid_forget()

        # If loop used here for toggling the dropdown menu
        # User clicks an opened subject, code will skip and reset (closing).
        if hasattr(self, 'last_opened') and self.last_opened == subject_code:
            self.last_opened = None
            return

        self.last_opened = subject_code
        # Used the same loop from creditpg.py v3, for the idea of the user manually inputted their grade
        for a, assessment in enumerate(assessments.get(subject_code, [])):
            for col, value in enumerate(assessment):
                if col == 2:
                    grade_entry = ctk.CTkEntry(table_frame)
                    grade_entry.grid(row=row + a + 1, column=col + 1, padx=10, pady=10)
                    self.grade_entries[f"{subject_code}_{a}"] = grade_entry
                else:
                    ctk.CTkLabel(table_frame, text=value).grid(row=row + a + 1, column=col + 1, padx=10, pady=10)

        ctk.CTkButton(table_frame, text="Save Grades", command=self.save_grades).grid(
            row=row + len(assessments.get(subject_code, [])) + 1, columnspan=5, pady=10)

    # Function to add the credits and save the grade in the table
    def save_grades(self):
        for key, entry in self.grade_entries.items():
            subject_code, index = key.split('_')
            grade = entry.get().strip().upper()
            index = int(index)

            # Determining credits achieved based on grade inputted by the user
            credits_available = self.assessments[subject_code][index][1]
            if grade == "NA":
                credits_achieved = 0
            elif grade == "A":
                credits_achieved = credits_available
            elif grade == "M":
                credits_achieved = credits_available
            elif grade == "E":
                credits_achieved = credits_available
            else:
                credits_achieved = 0
                # Default to 0 if an invalid grade is entered

            # Update the corresponding assessment data with the entered grade and credits achieved
            self.assessments[subject_code][index][2] = grade
            self.assessments[subject_code][index][3] = credits_achieved

    def add_credits(self):
        pass


if __name__ == "__main__":
    # Example student ID to fetch details
    student_id = "22656"
    CreditSummaryWindow(student_id)
