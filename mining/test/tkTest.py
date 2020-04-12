from tkinter import *


root = Tk()
off_color = "#ecbb06"
on_color = "green"


def on_check():  # this function will run on click on checkbutton
    if cbVar.get() == "1":
        chbox["bg"] = on_color  # if (get current checkbutton state) is "1" then....
    else:
        chbox["bg"] = off_color


cbVar = StringVar(root)  # making variable for checkbutton
cbVar.set(0)  # turning off the checkbutton (initialy)
chbox = Checkbutton(root,
                    variable=cbVar, text="Check me",
                    command=on_check, fg=off_color)  # making the checkbutton
chbox.place(x=0, y=0)  # placing the checkbutton
mainloop()
