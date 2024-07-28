import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pandas as pd

# Setting the appearance mode of CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Credit Table")
root.geometry("800x600")

# Set up the database
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS user_input
          (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT, user_grade TEXT)
          ''')
conn.commit()


def update_user_grade(user_id, user_grade):
    c.execute('''
              UPDATE user_input SET user_grade = ? WHERE id = ?
              ''', (user_grade, user_id))
    conn.commit()


def refresh_table():
    for widget in table_frame.winfo_children():
        widget.destroy()

    df = pd.read_sql_query("SELECT * FROM user_input", conn)
    for i, column in enumerate(df.columns):
        label = ctk.CTkLabel(table_frame, text=column)
        label.grid(row=0, column=i)
    for i, row in df.iterrows():
        for j, value in enumerate(row):
            if j == len(row) - 1:  # If it's the last column (user_grade)
                entry = ctk.CTkEntry(table_frame)
                entry.insert(0, value)
                entry.grid(row=i + 1, column=j)
                entry.bind("<Return>", lambda event, id=row['id']: update_grade(event, id))
            else:
                label = ctk.CTkLabel(table_frame, text=value)
                label.grid(row=i + 1, column=j)


def update_grade(event, user_id):
    entry = event.widget
    new_grade = entry.get()
    update_user_grade(user_id, new_grade)
    messagebox.showinfo("Update", f"Grade updated to {new_grade}")


# Entry fields
entry_name = ctk.CTkEntry(root, placeholder_text="Name")
entry_name.pack(pady=10)

entry_age = ctk.CTkEntry(root, placeholder_text="Age")
entry_age.pack(pady=10)

entry_email = ctk.CTkEntry(root, placeholder_text="Email")
entry_email.pack(pady=10)

entry_grade = ctk.CTkEntry(root, placeholder_text="Grade")
entry_grade.pack(pady=10)


def add_entry():
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    grade = entry_grade.get()

    if name and age and email and grade:
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Input Error", "Age must be an integer")
            return

        c.execute('''
                  INSERT INTO user_input (name, age, email, user_grade) VALUES (?, ?, ?, ?)
                  ''', (name, age, email, grade))
        conn.commit()

        refresh_table()

        entry_name.delete(0, 'end')
        entry_age.delete(0, 'end')
        entry_email.delete(0, 'end')
        entry_grade.delete(0, 'end')
    else:
        messagebox.showerror("Input Error", "All fields are required")


# Add button
add_button = ctk.CTkButton(root, text="Add Entry", command=add_entry)
add_button.pack(pady=20)

# Table frame
table_frame = ctk.CTkFrame(root)
table_frame.pack(pady=20, fill="both", expand=True)

refresh_table()

root.mainloop()

# Close the database connection when the program ends
conn.close()
