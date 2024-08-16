import customtkinter as ctk
import sqlite3


def fetch_grade_data():
    # Connect to the database
    conn = sqlite3.connect('../users.db')
    cursor = conn.cursor()

    # Fetch the data
    cursor.execute("SELECT grade, credits FROM grades")
    grade_data = cursor.fetchall()

    conn.close()
    return grade_data


def calculate_scores(grade_data):
    # Initialize counters
    excellence_credits = 0
    merit_credits = 0
    achieved_credits = 0

    for grade, credits in grade_data:
        if grade == 'E':
            excellence_credits += credits
        elif grade == 'M':
            merit_credits += credits
        elif grade == 'A':
            achieved_credits += credits

    # Calculate Best 80 Credits
    total_credits = excellence_credits + merit_credits + achieved_credits

    # Start by selecting all Excellence credits
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

    # Calculate Rank Scores
    rank_score_excellence = best_excellence_credits * 4
    rank_score_merit = best_merit_credits * 3
    rank_score_achieved = best_achieved_credits * 2

    total_rank_score = rank_score_excellence + rank_score_merit + rank_score_achieved

    return (
        excellence_credits, merit_credits, achieved_credits,
        best_excellence_credits, best_merit_credits, best_achieved_credits,
        rank_score_excellence, rank_score_merit, rank_score_achieved,
        total_rank_score
    )


def create_summary_table():
    # Fetch and calculate the data
    grade_data = fetch_grade_data()
    (
        excellence_credits, merit_credits, achieved_credits,
        best_excellence_credits, best_merit_credits, best_achieved_credits,
        rank_score_excellence, rank_score_merit, rank_score_achieved,
        total_rank_score
    ) = calculate_scores(grade_data)

    # Create the CustomTkinter window
    root = ctk.CTk()
    root.title("Credit Summary Table")

    # Create the table structure
    headers = ["", "Excellence Credits", "Merit Credits", "Achieved Credits"]
    data = [
        ["Number of Credits", excellence_credits, merit_credits, achieved_credits],
        ["Best 80 Credits", best_excellence_credits, best_merit_credits, best_achieved_credits],
        ["Rank Score", rank_score_excellence, rank_score_merit, rank_score_achieved],
        ["Total Rank Score", total_rank_score, "", ""]
    ]

    for i, header in enumerate(headers):
        label = ctk.CTkLabel(root, text=header, anchor="w")
        label.grid(row=0, column=i, padx=10, pady=5, sticky="w")

    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            label = ctk.CTkLabel(root, text=value, anchor="w")
            label.grid(row=row_index + 1, column=col_index, padx=10, pady=5, sticky="w")

    root.mainloop()


create_summary_table()
