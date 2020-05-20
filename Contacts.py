import tkinter as tk
import os
import csv
from tkinter import ttk
from tkinter import Frame, Grid, PhotoImage, Toplevel, messagebox as mBox
from time import sleep
import keyring
import re

# TODO keychain account will be computer username

class Login(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        # Instanciate Tk and set title
        self.window = master
        self.window.title("Login")
        self.credentials = False

        # create the widgets
        self.create_widgets()

        # set focus to where pin has to be inserted
        self.username_entry.focus()

    def retrieve_keychain(self):
        self.username = self.username_string.get()
        self.account = os.environ.get('USER')

        # retrieve username & password
        self.account_name = keyring.get_credential(self.username, self.account)
        if self.account_name == None:
            mBox.showwarning('No match', "No keychain entry with the name \"{0}\".".format(self.username))

    def check_credentials(self):
        # TODO extend to check account and password
        if self.account_name != None:
            if self.account_name.password == self.pass_string.get():
                self.credentials = True
            elif self.account_name.password != self.pass_string.get():
                mBox.showwarning('Wrong credentials', 'Wrong password. Please try again.')
                self.credentials = False

    def enter_clicked(self, arg=None):
        if self.check_var.get() == 1:
            self.open_toplevel()
        elif len(self.username_string.get()) != 0:
            if self.check_var.get() == 0:
                self.retrieve_keychain()
                self.check_credentials()
            if self.credentials:
                self.open_main_window()
        else:
            mBox.showwarning('Wrong credentials', 'No credentials entered. Please try again.')

    def open_toplevel(self):
        self.new_user = New_User()

    def open_main_window(self):
        self.window.quit()
        self.window.destroy()
        contacts = Contacts()
        contacts.window.mainloop()

    def create_widgets(self):
        # when 'Return' is pressed, it has the same effect as clicking 'Submit' button
        self.window.bind('<Return>', self.enter_clicked)

        self.username_string = tk.StringVar()
        self.pass_string = tk.StringVar()
        self.check_var = tk.IntVar()
        #self.pin_check = tk.StringVar()

        self.info_label = ttk.Label(self.window, text="Please enter name and passwrod or create a new one", wraplength=200)
        self.info_label.grid(column=0, row=0, columnspan=2)
        self.username_label = ttk.Label(self.window, text="Name")
        self.username_label.grid(column=0, row=1)
        self.username_entry = ttk.Entry(self.window, textvariable=self.username_string)
        self.username_entry.grid(column=1, row=1)
        self.password_label = ttk.Label(self.window, text="Password")
        self.password_label.grid(column=0, row=2)
        self.password_entry = ttk.Entry(self.window, textvariable=self.pass_string, show="\u2022")
        self.password_entry.grid(column=1, row=2)
        self.new_user_check = tk.Checkbutton(self.window, text="New user?", variable=self.check_var, onvalue=1, offvalue=0)
        self.new_user_check.deselect()
        self.new_user_check.grid(column=0, row=3)
        self.enter_button = ttk.Button(self.window, text="Enter", command=self.enter_clicked)
        self.enter_button.grid(column=1, row=3)

class Contacts():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Contacts")

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        # used if user has multiple accounts from the same provider
        self.counter = 2

        self.create_widgets()
        self.read_csv()
        self.detached = self.tree.get_children()

    def create_widgets(self):
        # create a frame to hold all the widgets
        self.frame = tk.Frame(self.window)
        self.frame.grid(column=0, row=0, sticky='new', padx=10, pady=10)
        self.frame.rowconfigure(4, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        # create buttons
        self.new_button = ttk.Button(self.frame, text="New", command=self.new_button_clicked)
        self.new_button.grid(column=0, row=0)
        self.edit_button = ttk.Button(self.frame, text="Edit", command=self.edit_button_clicked)
        self.edit_button.grid(column=1, row=0)

        # create entry form
        # create variables for entries and search
        self.account = tk.StringVar()
        self.user_id = tk.StringVar()
        self.password = tk.StringVar()
        self.search = tk.StringVar()
        self.search.trace('w', self.search_name)

        # create widgets for entry form
        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.grid(column=0, row=1, columnspan=2, pady=10)
        self.username_label = ttk.Label(self.form_frame, text="Name")
        self.username_label.grid(column=0, row=0)
        self.userid_label = ttk.Label(self.form_frame, text="User Id")
        self.userid_label.grid(column=0, row=1)
        self.password_label = ttk.Label(self.form_frame, text="Password")
        self.password_label.grid(column=0, row=2)
        self.username_entry = ttk.Entry(self.form_frame, textvariable=self.account, state='disabled')
        self.username_entry.grid(column=1, row=0)
        self.user_id_entry = ttk.Entry(self.form_frame, textvariable=self.user_id, state='disabled')
        self.user_id_entry.grid(column=1, row=1)
        self.password_entry = ttk.Entry(self.form_frame, textvariable=self.password, state='disabled')
        self.password_entry.grid(column=1, row=2)
        self.submit_button = ttk.Button(self.form_frame, text="Submit", command=self.submit_button_clicked, state='disabled')
        self.submit_button.grid(column=0, row=3, columnspan=2)

        # create search label and entry
        self.search_label = ttk.Label(self.frame, text="Search by name")
        self.search_label.grid(column=0, row=2, columnspan=2)
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search)
        self.search_entry.grid(column=0, row=3, columnspan=2)

        # create a Treeview
        self.tree = ttk.Treeview(self.frame, columns=('Name','UserId','Password'))
        self.tree.grid(column=0, row=4, columnspan=2, sticky='wne', padx=10, pady=10)
        # self.s = ttk.Scrollbar(self.tree, orient=tk.VERTICAL)
        # self.s.pack(side=tk.RIGHT, fill=tk.Y)
        # self.tree.configure(yscrollcommand=self.s.set)

        # set title, size of Treeview columns
        self.tree.column('#0', width=50, anchor='center')
        #self.tree.heading('#0', text='Name')
        self.tree.column('Name', width=100, anchor='center')
        self.tree.heading('Name', text='Name')
        self.tree.column('UserId', width=150, anchor='center')
        self.tree.heading('UserId', text='User Id')
        self.tree.column('Password', width=150, anchor='center')
        self.tree.heading('Password', text='Password')

    def new_button_clicked(self):
        self.username_entry.configure(state='enabled')
        self.user_id_entry.configure(state='enabled')
        self.password_entry.configure(state='enabled')
        self.submit_button.configure(state='enabled')
        self.account.set("")
        self.user_id.set("")
        self.password.set("")

    def edit_button_clicked(self, event=None):
        # enable entry widgets for editing
        try:
            # get the selected item
            item = self.tree.selection()[0]

            self.username_entry.configure(state='enabled')
            self.user_id_entry.configure(state='enabled')
            self.password_entry.configure(state='enabled')
            self.submit_button.configure(state='enabled')

            # fill entry widgets with data
            self.account.set(self.tree.item(item)['values'][0])
            self.user_id.set(self.tree.item(item)['values'][1])
            self.password.set(self.tree.item(item)['values'][2])
        except:
            mBox.showwarning("Selection", "No selection has been made. Please select a Name for editing.")

    def submit_button_clicked(self):
        # get the last element from the tree
        last = self.detached[-1]
        # last element incremented is the next element iid
        iid = int(last) + 1
        # TODO test see if iid could be used as index
        if len(self.account.get()) != 0 and len(self.user_id.get()) != 0 and len(self.password.get()) != 0:
            self.tree.insert('', self.index, iid, text=iid, values=(self.account.get(), self.user_id.get(), self.password.get()))
            self.write_to_csv(iid)
            self.detached = self.tree.get_children()
            self.clear_entries()
        else:
            mBox.showwarning('Entry missing', 'At least one entry is missing. Please check again.')

    def write_to_csv(self, iid):
        # write at the end of the csv file
        file = open('Contacts.csv', 'a')
        contacts = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        contacts.writerow([iid, self.account.get(), self.user_id.get(), self.password.get()])
        file.close()

        # TODO if row selected for editing, update row, don't insert new one

    def read_csv(self):
        fName = "Contacts.csv"
        try:
            file = open(fName)
            contacts = csv.reader(file)
            #self.index = 1
            for row in contacts:
                self.index = row[0]
                self.account.set(row[1])
                self.user_id.set(row[2])
                self.password.set(row[3])
                self.tree.insert('', 'end', self.index, text=self.index, values=(self.account.get(), self.user_id.get(), self.password.get()))
                self.clear_entries()
                #self.index += 1
            file.close()
        except IOError:
            print("No such file", fName)

    def clear_entries(self):
         # clear entry variables
        self.account.set("")
        self.user_id.set("")
        self.password.set("")
        # disable entries
        self.username_entry.configure(state='disabled')
        self.user_id_entry.configure(state='disabled')
        self.password_entry.configure(state='disabled')
        self.submit_button.configure(state='disabled')

    def search_name(self,*args):
        pattern = self.search.get()
        if len(self.search.get()) != 0:
            for item in self.detached:
                name = self.tree.item(item, option='values')[0]
                if not re.search(pattern.lower(), name.lower()):
                    self.tree.detach(item)
        else:
            for item in self.detached:
                self.tree.reattach(item, '', 'end')

class New_User(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        # TODO add window member
        self.grab_set()

        self.create_widgets()

    def button_clicked(self):
        if self.pass_string.get() != self.verify_pass_string.get() or len(self.pass_string.get()) == 0:
            mBox.showwarning('Missing credentials', 'Passwords are not identical or not entered. Please check again.')
        elif len(self.name_string.get()) == 0 or len(self.pass_string.get()) == 0:
            mBox.showwarning('Missing credentials', 'Name or name is missing. Please enter one.')
        else:
            # TODO set entries from login page with the newly created name details
            self.create_new_keychain()
            self.grab_release()
            self.destroy()
            if self.winfo_exists() == 0:
                login.username_entry.focus()
                login.check_var.set(0)
                login.username_string.set(self.name_string.get())
                login.pass_string.set(self.pass_string.get())

    def create_widgets(self):
        self.name_string = tk.StringVar()
        self.pass_string = tk.StringVar()
        self.verify_pass_string = tk.StringVar()

        self.info_label = ttk.Label(self, text="Enter name and password to create new entry", wraplength=200)
        self.info_label.grid(column=0, row=0, columnspan=2)
        self.name_label = ttk.Label(self, text="Name")
        self.name_label.grid(column=0, row=1)
        self.name_entry = ttk.Entry(self, textvariable=self.name_string)
        self.name_entry.grid(column=1, row=1)
        self.pass_label = ttk.Label(self, text="Password")
        self.pass_label.grid(column=0, row=2)
        self.pass_entry = ttk.Entry(self, textvariable=self.pass_string)
        self.pass_entry.grid(column=1, row=2)
        self.verify_pass_label = ttk.Label(self, text="Verify Password")
        self.verify_pass_label.grid(column=0, row=3)
        self.verify_pass_entry = ttk.Entry(self, textvariable=self.verify_pass_string)
        self.verify_pass_entry.grid(column=1, row=3)
        self.button = ttk.Button(self, text="Exit", command=self.button_clicked)
        self.button.grid(column=1, row=4)

    def create_new_keychain(self):
        keychain_name = self.name_string.get()
        account_name = os.environ.get('USER')
        password = self.pass_string.get()

        details = keyring.get_credential(keychain_name, account_name)
        if details == None:
            # store username & password
            keyring.set_password(keychain_name, account_name, password)
        else:
            mBox.showwarning('Credentials', 'Credentials alredy exist.')

# Start main loop
if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    login.window.mainloop()
