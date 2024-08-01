import customtkinter as ctk
from tkinter import messagebox
import sqlite3

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
        self.root.geometry("800x600")

        # Fetch data from the database
        result = fetch_subject_details(student_id)
        if result:
            year_level, subjects = result
            self.create_gui(year_level, subjects)
        else:
            messagebox.showinfo("", "Student ID not found.")
            self.root.destroy()

        self.root.mainloop()

    def create_gui(self, year_level, subjects):
        # Sample subject details mapping (Replace with actual data fetching logic)
        subject_details = {
            "13MAT": "NCEA Level 3 Mathematics (Calculus)",
            "13ENG": "NCEA Level 3 English",
            "13PHY": "NCEA Level 3 Physics",
            # Add other subjects as needed
        }

        # Labels
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(self.root, text="NCEA Credit Summary", font=title_font).pack(pady=20)

        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(pady=20, padx=20, fill="both", expand=True)

        headers = ["Subject Code", "Assessment Type", "Credits Available", "Grade Achieved", "Credits Achieved"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=title_font).grid(row=0, column=col, padx=10, pady=10)

        # Sample data to show (Replace with actual data fetching logic)
        assessments = {
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

        for row, subject_code in enumerate(subjects, start=1):
            full_subject = f"{year_level}{subject_code} - {subject_details.get(f'{year_level}{subject_code}', 'Unknown Subject')}"
            subject_label = ctk.CTkLabel(table_frame, text=full_subject)
            subject_label.grid(row=row, column=0, padx=10, pady=10)

            subject_label.bind("<Button-1>", lambda e, sc=f"{year_level}{subject_code}", r=row: self.toggle_assessment_display(sc, r, table_frame, assessments))

    def toggle_assessment_display(self, subject_code, row, table_frame, assessments):
        for widget in table_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > row:
                widget.grid_forget()

        if hasattr(self, 'last_opened') and self.last_opened == subject_code:
            self.last_opened = None
            return

        self.last_opened = subject_code
        for i, assessment in enumerate(assessments.get(subject_code, [])):
            for col, value in enumerate(assessment):
                if col == 2:  # If it's the "Grade Achieved" column
                    grade_entry = ctk.CTkEntry(table_frame)
                    grade_entry.grid(row=row + i + 1, column=col + 1, padx=10, pady=10)
                    self.grade_entries[f"{subject_code}_{i}"] = grade_entry
                else:
                    ctk.CTkLabel(table_frame, text=value).grid(row=row + i + 1, column=col + 1, padx=10, pady=10)

        ctk.CTkButton(table_frame, text="Save Grades", command=self.save_grades).grid(row=row + len(assessments.get(subject_code, [])) + 1, columnspan=5, pady=10)

    def save_grades(self):
        for key, entry in self.grade_entries.items():
            subject_code, index = key.split('_')
            grade = entry.get()
            # Update the corresponding assessment data with the entered grade
            assessments[subject_code][int(index)][2] = grade
            # Logic to save the grades to the database can be added here
            print(f"Saved {grade} for {subject_code} assessment {index}")

    def add_credits(self):
        # Logic to add credits
        pass

if __name__ == "__main__":
    # Example student ID to fetch details
    student_id = "22656"
    CreditSummaryWindow(student_id)
