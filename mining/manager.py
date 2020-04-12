import sys
from tkinter import messagebox
import tkinter as tk
import tkinter.font as tk_font

from crawler import Stock


# from database import Database


# # Currently Unavailable
# from stock_data import database as db
#
# # Instantiate database object
# database = db.Database('store.db')

class ConsoleText(tk.Text):
	"""A Tkinter Text widget that provides a scrolling display of console stdout."""


	class StdoutRedirector(object):
		"""A class for redirecting stdout to this Text widget."""

		def __init__(self):
			self.buff = ''
			self.__console__ = sys.stdout

		def write(self, output_stream):
			self.buff += output_stream

		def to_console(self):
			sys.stdout = self.__console__
			print(self.buff)

		def flush(self):
			self.buff = ''

		def reset(self):
			sys.stdout = self.__console__


	def __init__(self, master=None, cnf={}, **kw):
		tk.Text.__init__(self, master, cnf, **kw)
		self.tag_configure('STDOUT',
		                   background='#404040',
		                   foreground='#cc9900')
		self.original_stdout = sys.stdout  # Save the original stdout for recovery
		self.stdout_redirect = ConsoleText.StdoutRedirector()
		sys.stdout = self.stdout_redirect

	def restart(self):
		sys.stdout = self.original_stdout
		self.stdout_redirect.flush()
		sys.stdout = self.stdout_redirect

	def write(self, val):
		self.stdout_redirect.write(val)
		self.see('end')


class Application(tk.Frame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		master.title('Stock')
		master.geometry("600x800")
		ft = tk_font.Font(family='Consolas', size=12)
		self.styleSet = {'padx': 10,
		                 'pady': 10,
		                 'relief': tk.FLAT,
		                 'font': ft}
		self.create_widgets()

	# self.selected_item = 0  # Init selected item var
	# self.populate_list()  # Populate initial list

	def create_widgets(self):
		# Section Title
		crawler_label = tk.Label(self.master, text='CRAWLER', **self.styleSet)
		crawler_label.grid(row=0, column=0)

		# Year Input
		year_label = tk.Label(self.master, text='Year', **self.styleSet)
		year_label.grid(row=1, column=0)
		self.year_text = tk.StringVar()
		self.year_entry = tk.Entry(self.master, textvariable=self.year_text)
		self.year_entry.grid(row=1, column=1)
		self.year_entry.bind('<FocusIn>', self.on_focusin_year)
		self.year_entry.bind('<FocusOut>', self.on_focusout_year)
		self.on_focusout_year()

		# # TODO
		# self.year_sel = tk.IntVar
		# self.all_year = tk.Spinbox(self.master, from_=2010, to=2019, textvariable=self.year_sel)
		# self.all_year.grid(row=1, column=2, padx=20)

		# Quarter Input
		quarter_label = tk.Label(self.master, text='Quarter', **self.styleSet)
		quarter_label.grid(row=2, column=0)
		self.quarter_text = tk.StringVar()
		self.quarter_entry = tk.Entry(self.master, textvariable=self.quarter_text)
		self.quarter_entry.grid(row=2, column=1)
		self.quarter_entry.bind('<FocusIn>', self.on_focusin_quarter)
		self.quarter_entry.bind('<FocusOut>', self.on_focusout_quarter)
		self.on_focusout_quarter()

		# Table Input
		table_label = tk.Label(self.master, text='Table', **self.styleSet)
		table_label.grid(row=3, column=0)
		self.table_text = tk.StringVar()
		self.table_entry = tk.Entry(self.master, textvariable=self.table_text)
		self.table_entry.grid(row=3, column=1)
		self.table_entry.bind('<FocusIn>', self.on_focusin_table)
		self.table_entry.bind('<FocusOut>', self.on_focusout_table)
		self.on_focusout_table()

		# Random check box
		self.randomize = tk.IntVar()
		self.random_check = tk.Checkbutton(self.master, text='Randomize',
		                                   relief=tk.RAISED,
		                                   activebackground='#edd57e',
		                                   onvalue=1, offvalue=0,
		                                   command=self.switch,
		                                   variable=self.randomize)
		self.randomize.set(0)
		self.random_check.grid(row=0, column=1)

		# Button
		crawl_btn = tk.Button(self.master, text='crawl', command=self.get_crawl)
		crawl_btn.grid(row=4, column=0, padx=10)
		reset_btn = tk.Button(self.master, text='reset', command=self.reset_text)
		reset_btn.grid(row=5, column=0, padx=10)
		clear_btn = tk.Button(self.master, text='clear', command=self.clear_text)
		clear_btn.grid(row=6, column=0, padx=10)

		# Text box to redirect stdout
		self.output = ConsoleText(self.master, height=10, width=20)
		self.output.grid(row=4, column=1, rowspan=4, sticky=tk.W)

	# # List
	# table_list = tk.Listbox(self.master)
	# table_list.grid(row=4, column=2,
	#                 rowspan=3, columnspan=3,
	#                 pady=10, padx=10,
	#                 sticky=tk.E)
	# scrollbar = tk.Scrollbar(self.master)
	# scrollbar.grid(row=4, column=4)
	# table_list.configure(yscrollcommand=scrollbar)
	# scrollbar.configure(command=table_list.yview)

	def clear_text(self):
		self.output.restart()

	def get_crawl(self):
		if int(self.randomize.get()) == 1:
			stock_crawler = Stock(random_query=True)
			return

		try:
			year = int(self.year_text.get())
			quarter = str(self.quarter_text.get())
			table = int(self.table_text.get())
			stock_crawler = Stock(random_query=False,
			                      year_query=year,
			                      quarter_query=quarter,
			                      table_query=table)
		except Exception as e:
			messagebox.showerror("Required Fields", e)
			self.clear_text()
			return

		stock_crawler.run_query()

	def reset_text(self):
		self.year_entry.delete(0, tk.END)
		self.quarter_entry.delete(0, tk.END)
		self.table_entry.delete(0, tk.END)
		self.on_focusout_year()
		self.on_focusout_quarter()
		self.on_focusout_table()
		if int(self.randomize.get()) == 1:
			self.random_check.invoke()
			self.random_check.deselect()

	def switch(self):
		if int(self.randomize.get()) == 1:
			self.random_check['bg'] = '#ecbb06'
		else:
			self.random_check['bg'] = '#f0f0f0'

	def on_focusin_year(self, event=None):
		if self.year_entry.get() == '2010-2019':
			self.year_entry.delete(0, "end")  # delete all the text in the entry
			self.year_entry.insert(0, '')  # Insert blank for user input
			self.year_entry.config(fg='black')

	def on_focusin_quarter(self, event=None):
		if self.quarter_entry.get() == '03/06/09/12':
			self.quarter_entry.delete(0, "end")  # delete all the text in the entry
			self.quarter_entry.insert(0, '')  # Insert blank for user input
			self.quarter_entry.config(fg='black')

	def on_focusin_table(self, event=None):
		if self.table_entry.get() == '1-7':
			self.table_entry.delete(0, "end")  # delete all the text in the entry
			self.table_entry.insert(0, '')  # Insert blank for user input
			self.table_entry.config(fg='black')

	def on_focusout_quarter(self, event=None):
		if self.quarter_entry.get() == '':
			self.quarter_entry.insert(0, '03/06/09/12')
			self.quarter_entry.config(fg='grey')

	def on_focusout_table(self, event=None):
		if self.table_entry.get() == '':
			self.table_entry.insert(0, '1-7')
			self.table_entry.config(fg='grey')

	def on_focusout_year(self, event=None):
		if self.year_entry.get() == '':
			self.year_entry.insert(0, '2010-2019')
			self.year_entry.config(fg='grey')


# Activate
root = tk.Tk()
app = Application(master=root)
app.mainloop()
