from tkinter import *

# Window object
app = Tk()

part_text = StringVar()
part_label = Label(app, text='Try', font=('bold', 14), pady=14)
part_label.grid(row=0, column=0, sticky=W)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=10)


app.title('Part Manager')
app.geometry('800x600')


app.mainloop()
