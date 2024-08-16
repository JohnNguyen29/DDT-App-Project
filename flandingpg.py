"""This file is the home page or landing page for my app, Next Steps."""
import customtkinter
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import subprocess
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_grades_data(student_id):
    """Function to fetch the users grades data such as student ID
    and sum of credits from 'user.db'
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

def fetch_grade_data():
    """Function to fetch only the grades and
    credits in 'grades' table in users.db
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT grade, credits FROM grades")
    grade_data = cursor.fetchall()

    conn.close()
    return grade_data

class HomePage:
    """Using a class for the home/landing page because it is its own window
    Able to store mulitple functions for feature of the GUI and app
    """
    def __init__(self, student_id):
        """Creating the window based on the student_id
        """
        self.student_id = student_id
        self.root = ctk.CTk()
        self.root.title("NextSteps Home Page")
        self.root.geometry("1440x900")

        # Appearance mode of CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Navigation frame
        nav_frame = ctk.CTkFrame(self.root, width=200)
        nav_frame.pack(side="left", fill="y")

        self.logo_image(nav_frame)

        # Navigation buttons
        buttons = [
            ("Home", None),
            ("Credit Summary", self.open_credit_summary),
            ("Course Search", self.open_course_search),
        ]

        for button_text, command in buttons:
            button = ctk.CTkButton(nav_frame, text=button_text, width=150,
                                   command=command)
            button.pack(pady=10)

        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Welcome frame at the top
        self.welcome_frame = ctk.CTkFrame(self.main_frame, height=100)
        self.welcome_frame.pack(side="top", fill="x")

        # Top frame
        self.top_frame = ctk.CTkFrame(self.main_frame)
        self.top_frame.pack(side="top", fill="both", pady=10)

        # Bottom frame
        self.bottom_frame = ctk.CTkFrame(self.main_frame, height=200)
        self.bottom_frame.pack(fill="x")

        # Create the GUI elements in the frames
        self.create_gui(self.welcome_frame, self.top_frame, self.bottom_frame)
        self.root.mainloop()

    def logo_image(self, nav_frame):
        """Function to display the logo image on the navigation bar
        """
        my_img = Image.open("/Users/nguyennguyen/Desktop/DDT/NSLogo.png")
        resized = my_img.resize((200, 200), Image.LANCZOS)
        new_pic = ImageTk.PhotoImage(resized)
        label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
        label.image = new_pic
        label.pack()

    # Function to run/redirect user to the landing page when button is clicked
    def open_course_search(self):
        """Function to run/redirect user to the
        landing page when button is clicked
        """
        self.root.destroy()
        subprocess.run(["python3", "fcoursesearchpg.py", self.student_id])

    # Function to redirect to the credit summary page
    def open_credit_summary(self):
        """Function to redirect to the credit summary page
        """
        self.root.destroy()
        subprocess.run(["python3", "fcreditpg.py", self.student_id])

    def create_gui(self, welcome_frame, top_frame, bottom_frame):
        """ Function to create the pages GUI"""
        # Welcome message in the welcome frame
        title_font = ctk.CTkFont(size=20, weight="bold")
        ctk.CTkLabel(welcome_frame, text="Welcome! This is your NCEA summary...",
                     font=title_font).pack(pady=20)

        # Bottom frame content
        self.display_bookmarked_courses(bottom_frame)

        ctk.CTkButton(self.top_frame, text="Show NCEA Progress",
                      command=self.update_pie_chart).pack(pady=10)

    def calculate_scores(self, grade_data):
        """Calculating the rank score based on the grade_data
        the user has inputted in fcreditspg.py which is
        stored in the 'grades' table in 'user's db'
        """
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
        """Function to update the pie chart when the user enters a grade
        Modified function to update the pie chart and progress bars
        """
        # Clear any existing widgets in top_frame
        for widget in self.top_frame.winfo_children():
            widget.destroy()

        # Configure grid layout for top_frame
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=2)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)

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

        # Left side: Progress Bars
        progress_bar_frame = ctk.CTkFrame(self.top_frame)
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
        rank_score_frame = ctk.CTkFrame(self.top_frame)
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

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(rank_score_frame, text=header, anchor="w")
            label.grid(row=0, column=i, padx=10, pady=5, sticky="w")

        for row_index, row in enumerate(data):
            for col_index, value in enumerate(row):
                label = ctk.CTkLabel(rank_score_frame, text=value, anchor="w")
                label.grid(row=row_index + 1, column=col_index, padx=10, pady=5, sticky="w")

        # Right Side: Pie Chart
        pie_top_frame = ctk.CTkFrame(self.top_frame)
        pie_top_frame.grid(row=0, column=2, padx=20, pady=10, sticky="nsew")

        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie([achieved_credits, merit_credits, excellence_credits],
               labels=["Achieved", "Merit", "Excellence"], autopct='%1.1f%%', startangle=90)

        chart = FigureCanvasTkAgg(fig, master=pie_top_frame)
        chart.get_tk_widget().pack(expand=True, fill="both")

        chart.draw()

    def create_progress_bar(self, label_text, value, max_value, parent, total=False):
        """Function to create and update a
        progress bar with a parent frame parameter
        """
        label_font = ctk.CTkFont(size=14, weight="bold") if total else None
        ctk.CTkLabel(parent, text=f"{label_text} ({value}/{max_value})",
                     font=label_font).pack(pady=5)

        # Setting in minimum and maximum value for the progress bar
        progress_bar = ctk.CTkProgressBar(parent, height=30 if total else None)
        progress_bar.set(value / max_value)
        progress_bar.pack(pady=5, fill="x")

    def display_bookmarked_courses(self, frame):
        """Function to display bookmarked courses in the bottom frame
        Fetches bookmarks from the bookmarks table in 'users.db'
        """
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT course, university, subject FROM bookmarks")
        bookmarks = cursor.fetchall()

        conn.close()

        # If loop for when there is a bookmarked course in the table,
        # it will create a label for it with a remove button
        # that runs the remove_bookmark function
        if bookmarks:
            bookmark_label = ctk.CTkLabel(frame, text="Bookmarked Courses",
                                          font=("Arial", 16, "bold"))
            bookmark_label.pack(pady=10)

            for course, university, subject in bookmarks:
                bookmark_frame = ctk.CTkFrame(frame)
                bookmark_frame.pack(fill="x", pady=5)

                course_label = ctk.CTkLabel(bookmark_frame, text=course,
                                            font=("Arial", 14))
                course_label.pack(side="left")

                remove_button = ctk.CTkButton(bookmark_frame, text="Remove", width=100,
                                              command=lambda c=course: self.remove_bookmark(c))
                remove_button.pack(side="right")
        # Else it will show an error text on GUI
        else:
            no_bookmarks_label = ctk.CTkLabel(frame, text="No bookmarked courses.",
                                              font=("Arial", 14))
            no_bookmarks_label.pack(pady=20)

    def remove_bookmark(self, course):
        """Function to remove a bookmark
        Editing the table using DELETE and shows
        a message box that bookmark has been removed
        """
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bookmarks WHERE course=?", (course,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Bookmark Removed", f"Course '{course}' has been removed from bookmarks")
        self.display_bookmarked_courses(self.bottom_frame)  # Refresh the bookmark list

if __name__ == "__main__":
    #  Get student_id from command-line arguments
    student_id = sys.argv[1]
    HomePage(student_id)