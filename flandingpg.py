import tkinter as tk
from re import search


root = tk.Tk()
root.title("Landing Page")
root.geometry("1440x900")

# Bottom frame
bottom_frame = tk.Frame(root, bg="blue", width=400, height=450)
bottom_frame.pack(side="bottom", fill="x")

# Search bar for courses in bottom frame
label_searchbar = tk.Label(bottom_frame, text="Search courses:", font=("Helvetica", 18), fg="black")
label_searchbar.pack(pady=200, side="left")
entry_searchbar = tk.Entry(bottom_frame, width=60)
entry_searchbar.pack(pady=200, side="left")
button_searchbar = tk.Button(bottom_frame, text="Search", command=search)
button_searchbar.pack(pady=200, side="left")

root.mainloop()
