import customtkinter as ctk
from re import search
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image

# Setting the appearance mode of CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Landing Page")
root.geometry("1440x900")

def overlay_image():
    # Image
    my_img = Image.open("/Users/nguyennguyen/Desktop/templogo.png")
    resized = my_img.resize((200, 100), Image.LANCZOS)

    new_pic = ImageTk.PhotoImage(resized)

    label = ctk.CTkLabel(nav_frame, image=new_pic)
    label.image = new_pic
    label.pack()

# Navigation frame
nav_frame = ctk.CTkFrame(root, width=200, height=400)
nav_frame.pack(side="left", fill="y")

# Top frame
top_frame = ctk.CTkFrame(root, width=400, height=450)
top_frame.pack(side="top", fill="x")

# Bottom frame
bottom_frame = ctk.CTkFrame(root, width=400, height=450)
bottom_frame.pack(side="bottom", fill="x", expand = 10)

overlay_image()

# Navigation buttons
buttons = ["Home", "Credit Summary", "Course Search", "Help Centre"]

for button_text in buttons:
    button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=lambda b=button_text: navigate(b))
    button.pack(pady=10)

# Welcome text in top frame
text_label = ctk.CTkLabel(top_frame, text="Welcome! This is your current NCEA summary...", font=("Arial", 24), text_color="black")
text_label.pack(pady=50, padx=50, side="left")

# 3 Progress bars for NCEA credits in top frame
l1progress = ctk.CTkLabel(top_frame, text="Level 1 credits:", font=("Helvetica", 12), text_color="white")
l1progress.pack(pady=5, side="top")
progress_bar1 = ctk.CTkLabel(top_frame, fg_color="white", width=200, height=10)
progress_bar1.pack(pady=5, side="top")

l2progress = ctk.CTkLabel(top_frame, text="Level 2 credits:", font=("Helvetica", 12), text_color="white")
l2progress.pack(pady=5, side="top")
progress_bar2 = ctk.CTkLabel(top_frame, fg_color="white", width=200, height=10)
progress_bar2.pack(pady=5, side="top")

l3progress = ctk.CTkLabel(top_frame, text="Level 3 credits:", font=("Helvetica", 12), text_color="white")
l3progress.pack(pady=5, side="top")
progress_bar3 = ctk.CTkLabel(top_frame, fg_color="white", width=200, height=10)
progress_bar3.pack(pady=5, side="top")

# Pie chart for the current NCEA level progress
number_credits = [30, 20, 50]
grade = ['Achieved', 'Merit', 'Excellence']

fig, ax = plt.subplots(figsize=(3, 3))
ax.pie(number_credits, labels=grade, autopct='%1.1f%%')
ax.axis('equal')

canvas = FigureCanvasTkAgg(fig, master=top_frame)
canvas.draw()
canvas.get_tk_widget().pack()

# Search bar for courses in bottom frame
label_searchbar = ctk.CTkLabel(bottom_frame, text="Search courses:", font=("Helvetica", 18), text_color="black")
label_searchbar.pack(pady=20, side="left")
entry_searchbar = ctk.CTkEntry(bottom_frame, width=400)
entry_searchbar.pack(pady=20, side="left")
button_searchbar = ctk.CTkButton(bottom_frame, text="Search", command=search)
button_searchbar.pack(pady=20, side="left")

root.mainloop()
