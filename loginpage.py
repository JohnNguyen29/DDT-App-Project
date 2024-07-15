from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

connection = sqlite3.connect("users.db")
cursor =connection.cursor()

user_details_list = [
("Alexsmith" ,  "12AMAT"),
("Tessa McLaren" ,  "12BHAH"),
("Corey Toss" ,  "13RAAH"),
("Simon Solen" ,  "12YHAU"),
]

cursor.executemany("insert into user_details values (?,?)" , user_details_list)

#print database rows
for row in cursor.execute("select * from user_details "):
    print(row)
connection.commit()
connection.close()

def Ok():
    uname = e1.get()
    password = e2.get()

    if (uname == "" and password == ""):
        messagebox.showinfo("", "Blank Not allowed")


    elif (uname == "testuser" and password == "zzz"):
        messagebox.showinfo("", "Login Success")
        root.destroy()
        subprocess.run(["python3", "landingpage.py"])

    else:
        messagebox.showinfo("", "Incorrect Username and Password")


root = Tk()
root.title("NextSteps Login")
root.geometry("1440x900")
global e1
global e2

Label(root, text="Username").place(x=10, y=10)
Label(root, text="Password").place(x=10, y=40)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")

Button(root, text="Login", command=Ok, height=3, width=13).place(x=10, y=100)
Button(root, text="Register", command=Ok, height=3, width=13).place(x=10, y=180)

root.mainloop()