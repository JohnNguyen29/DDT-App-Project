import tkinter as tk
from re import search
from tkinter import *
from tkinter.ttk import Progressbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

root = tk.Tk()
root.title("Landing Page")
root.geometry("1440x900")

def overlay_image():
    # Image
    my_img = Image.open("/Users/nguyennguyen/Desktop/templogo.png")
    resized = my_img.resize((200, 100), Image.LANCZOS)

    new_pic = ImageTk.PhotoImage(resized)

    label = tk.Label(nav_frame, image=new_pic)
    label.image = new_pic
    label.pack()

# Navigation frame
nav_frame = tk.Frame(root, bg="white", width=200, height=400)
nav_frame.pack(side="left", fill="y")

# Top frame
top_frame = tk.Frame(root, bg="lightblue", width=400, height=450)
top_frame.pack(side="top", fill="x")

# Bottom frame
bottom_frame = tk.Frame(root, bg="blue", width=400, height=450)
bottom_frame.pack(side="bottom", fill="x")

overlay_image()

def navigate(page):
    print("Navigating...", page)

# Navigation buttons
buttons = ["Home", "Credit Summary", "Course Search", "Help Centre"]

for button_text in buttons:
    button = tk.Button(nav_frame, text=button_text, width=15, command=lambda b=button_text: navigate(b))
    button.pack(pady=10)

# Welcome text in top frame
text_label = tk.Label(top_frame, text="Welcome [name]! This is your NCEA summary...", font=("Arial", 24), bg="lightblue", fg="black")
text_label.pack(pady=50, padx=50, side="left")

# 3 Progress bars for NCEA credits in top frame
l1progress = tk.Label(top_frame, text="Level 1 credits:", font=("Helvetica", 12), fg="white")
l1progress.pack(pady=5, side="top")
progress_bar1 = tk.Label(top_frame, relief="ridge", bg="white", width=20, height=1)
progress_bar1.pack(pady=5, side="top")

l2progress = tk.Label(top_frame, text="Level 2 credits:", font=("Helvetica", 12), fg="white")
l2progress.pack(pady=5, side="top")
progress_bar2 = tk.Label(top_frame, relief="ridge", bg="white", width=20, height=1)
progress_bar2.pack(pady=5, side="top")

l3progress = tk.Label(top_frame, text="Level 3 credits:", font=("Helvetica", 12), fg="white")
l3progress.pack(pady=5, side="top")
progress_bar3 = tk.Label(top_frame, relief="ridge", bg="white", width=20, height=1)
progress_bar3.pack(pady=5, side="top")

# Pie chart for the current NCEA level progress
number_credits = [30, 20, 50]
grade = ['Achieved', 'Merit', 'Excellence']

fig, ax = plt.subplots(figsize=(3, 3), facecolor='lightblue')
ax.pie(number_credits, labels=grade, autopct='%1.1f%%')
ax.axis('equal')

canvas = FigureCanvasTkAgg(fig, master=top_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Search bar for courses in bottom frame
label_searchbar = tk.Label(bottom_frame, text="Search courses:", font=("Helvetica", 18), fg="black")
label_searchbar.pack(pady=200, side="left")
entry_searchbar = tk.Entry(bottom_frame, width=60)
entry_searchbar.pack(pady=200, side="left")
button_searchbar = tk.Button(bottom_frame, text="Search", command=search)
button_searchbar.pack(pady=200, side="left")

root.mainloop()