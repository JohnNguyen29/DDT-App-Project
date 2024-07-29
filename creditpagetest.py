import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import the PIL library
import sqlite3
import subprocess

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
        assessments = [
            ["Internal", 4, "A", 4],
            ["External", 5, "E", 5],
            ["Internal", 6, "M", 6],
            ["Internal", 3, "A", 3],
            ["Internal", 6, "M", 6],
            ["External", 4, "E", 4]
        ]

        for row, subject_code in enumerate(subjects, start=1):
            full_subject = f"{subject_code} - {subject_details.get(subject_code, 'Unknown Subject')}"
            ctk.CTkLabel(table_frame, text=full_subject).grid(row=row, column=0, padx=10, pady=10)

            for col, value in enumerate(assessments[row - 1]):
                ctk.CTkLabel(table_frame, text=value).grid(row=row, column=col + 1, padx=10, pady=10)

        ctk.CTkButton(self.root, text="Add Credits", command=self.add_credits).pack(pady=10)

    def add_credits(self):
        # Logic to add credits
        pass


if __name__ == "__main__":
    # Example student ID to fetch details
    student_id = "student123"
    CreditSummaryWindow(student_id)
