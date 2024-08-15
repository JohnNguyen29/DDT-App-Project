import tkinter as tk
from tkinter import *
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

overlay_image()

def navigate(page):
# Navigation buttons
buttons = ["Home", "Credit Summary", "Course Search", "Help Centre"]

for button_text in buttons:
    button = tk.Button(nav_frame, text=button_text, width=15, command=lambda b=button_text: navigate(b))
    button.pack(pady=10)

root.mainloop()
