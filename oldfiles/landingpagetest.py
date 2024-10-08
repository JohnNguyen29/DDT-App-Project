import customtkinter as ctk
import subprocess
from PIL import ImageTk, Image

# Setting the appearance mode of CustomTkinter
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Landing Page")
root.geometry("1440x900")

#
def overlay_image():
    # Logo image
    my_img = Image.open("/Users/nguyennguyen/Desktop/NSLogo.png")
    resized = my_img.resize((200, 200), Image.LANCZOS)

    new_pic = ImageTk.PhotoImage(resized)

    label = ctk.CTkLabel(nav_frame, image=new_pic, text="")
    label.image = new_pic
    label.pack()

# Function to open the credit page
def open_credit_summary():
    subprocess.run(["python3", "creditpg.py"])

# Function to open the course search page
def open_course_search():
    subprocess.run(["python3", "course_search.py"])

#Function to open the help center
def open_help_center():
    subprocess.run(["python3", "help_center.py"])

# Navigation frame
nav_frame = ctk.CTkFrame(root, width=200)
nav_frame.pack(side="left", fill="y")

overlay_image()

# Main content frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(side="right", fill="both", expand=True)

# Different pages as frames
home_frame = ctk.CTkFrame(main_frame)
course_search_frame = ctk.CTkFrame(main_frame)
help_center_frame = ctk.CTkFrame(main_frame)

for frame in (home_frame, course_search_frame, help_center_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Navigation buttons
buttons = [
    ("Home", None),
    ("Credit Summary", None),  # Button to open credit summary script
    ("Course Search", None),  # Button to open course search script
    ("Help Center", None)  # Button to open help center script
]
# For loop for all the buttons. Button placement on the frame and if clicked, the fucnction command coded above runs.
for button_text, frame in buttons:
    if frame:
        button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=lambda f=frame: show_frame(f))
    elif button_text == "Credit Summary":
        button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=open_credit_summary)
    elif button_text == "Course Search":
        button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=open_course_search)
    elif button_text == "Help Center":
        button = ctk.CTkButton(nav_frame, text=button_text, width=150, command=open_help_center)
    else:
        button = ctk.CTkButton(nav_frame, text=button_text, width=150)  # Default case
    button.pack(pady=10)

# Home frame content
text_label = ctk.CTkLabel(home_frame, text="WELCOME!", font=("Arial", 24), text_color="black")
text_label.pack(padx=20, pady=10)

# Course Search frame content
label_searchbar = ctk.CTkLabel(course_search_frame, text="BOOKMARKED COURSES", font=("Helvetica", 18), text_color="black")
label_searchbar.grid(row=0, column=0, padx=20, pady=10, columnspan=3)

# University selection
uni_label = ctk.CTkLabel(course_search_frame, text="Universities", font=("Helvetica", 14), text_color="black")
uni_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

uni_options = ["University of Auckland", "Massey University", "Otago University"]
var_unis = {uni: ctk.StringVar(value=0) for uni in uni_options}

for i, uni in enumerate(uni_options):
    checkbutton = ctk.CTkCheckBox(course_search_frame, text=uni, variable=var_unis[uni])
    checkbutton.grid(row=i+2, column=0, padx=20, pady=5, sticky="w")

# Search bar
entry_searchbar = ctk.CTkEntry(course_search_frame, width=400)
entry_searchbar.grid(row=1, column=1, padx=20, pady=10)
button_searchbar = ctk.CTkButton(course_search_frame, text="Search")
button_searchbar.grid(row=1, column=2, padx=20, pady=10)

# Bookmarked courses
course_frame = ctk.CTkFrame(course_search_frame)
course_frame.grid(row=2, column=1, columnspan=2, rowspan=4, padx=20, pady=10, sticky="nsew")

bookmarked_courses = [
    {"university": "University of Auckland", "course": "BSc - Bachelor of Science"},
    {"university": "University of Auckland", "course": "BE (Hons) - Bachelor of Engineering"}
]

for i, course in enumerate(bookmarked_courses):
    course_label = ctk.CTkLabel(course_frame, text=f'{course["university"]}\n{course["course"]}', font=("Helvetica", 12), text_color="black")
    course_label.pack(padx=20, pady=10, fill="x", expand=True)

# Help Center frame content
help_label = ctk.CTkLabel(help_center_frame, text="Help Center", font=("Helvetica", 24), text_color="black")
help_label.pack(padx=20, pady=20)

# Function to show selected frame
def show_frame(frame):
    frame.tkraise()

# Show the home frame initially
home_frame.tkraise()

root.mainloop()
