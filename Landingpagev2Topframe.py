import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.title("Landing Page")
root.geometry("1440x900")

# Top frame
top_frame = tk.Frame(root, bg="lightblue", width=400, height=450)
top_frame.pack(side="top", fill="x")

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

root.mainloop()
