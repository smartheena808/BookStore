"""
Bookstore App is a desktop app that is used to store book's information,
including: title, author, year, and ISBN.

Features that user can uses in this app:
- View all records
- Search an entry
- Add entry
- Update entry
- Delete entry
- Exit/Close app

This app is using Tkinter library for UI interface and postgresql for the database.
"""

from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
from smartDB import Database as db

class BookStore:    
    """ BookStore App
    """
    def __init__(self, master=None):
        # Create menubar
        self.master = master
        self.master.wm_title('BookStore')
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        # Create child menu
        self.file = Menu(self.menubar)
        # Add to menubar
        self.menubar.add_cascade(menu=self.file, label='File')
        # Create command menu for File
        self.file.add_separator
        self.file.add_command(label= 'Exit', command = quit)

        # Create Book's detail input frame, parent: master
        self.detailFrame = ttk.LabelFrame(master, text='Smart Bookstore', width=540, height=120)
        self.detailFrame.pack(fill=BOTH, expand=TRUE, padx=5, pady=5)

        # Create frame for view, parent: master
        self.viewFrame = ttk.Frame(master, width=500, height=150, relief= RIDGE)
        self.viewFrame.pack(fill= BOTH, expand=TRUE)        
        self.viewFrame.rowconfigure(0, weight = 3)
        self.viewFrame.columnconfigure(0, weight = 1)
        self.viewFrame.columnconfigure(1, weight = 1)
        
        # Create Control frame, parent: viewFrame
        self.controlFrame = ttk.LabelFrame(self.viewFrame, text='Control Navigation', 
                            width=200, height=250,)
        self.controlFrame.grid(row=0,column=2, padx=5, pady=5)
        # Create text to display the entry, parent: viewFrame
        self.viewEntryList = Listbox(self.viewFrame, width=60, height=15)
        self.viewEntryList.grid(row=0,column=0, padx=5, pady=5)
        self.viewEntryList.rowconfigure(0, weight= 1)
        self.viewEntryList.columnconfigure(0, weight= 1)

        # Create scrollbar for the list view
        self.yscrollbarlist = ttk.Scrollbar(self.viewFrame, orient= VERTICAL, command=self.viewEntryList.yview)
        self.xscrollbarlist = ttk.Scrollbar(self.viewFrame, orient= HORIZONTAL, command=self.viewEntryList.xview)
        self.yscrollbarlist.grid(row=0, column=1, sticky= 'ns', padx=5, pady=5)
        self.xscrollbarlist.grid(row=1, column=0, sticky= 'ew', padx=5, pady=5)
        # Attaches to viewEntry list
        self.viewEntryList.config(yscrollcommand= self.yscrollbarlist.set)
        self.viewEntryList.config(xscrollcommand= self.xscrollbarlist.set)

        # bind viewEntryList with an event
        self.viewEntryList.bind('<<ListboxSelect>>', self.get_selected_row)

        # Create 4 entries for input book's detail
        self.titleLabel = ttk.Label(self.detailFrame, text='Title: ', width=8)
        self.titleLabel.grid(row=0, column=0)
        self.authorLabel = ttk.Label(self.detailFrame, text='Author: ', width=10)
        self.authorLabel.grid(row=0,column=2)
        self.yearLabel = ttk.Label(self.detailFrame, text='Year: ', width=8)
        self.yearLabel.grid(row=1,column=0)
        self.isbnLabel = ttk.Label(self.detailFrame, text='ISBN: ', width=10)
        self.isbnLabel.grid(row=1,column=2)

        # Create variables for entries
        self.titleVar = StringVar(self.detailFrame)
        self.authorVar = StringVar(self.detailFrame)
        self.isbnVar = StringVar(self.detailFrame)
        self.yearVar = IntVar(self.detailFrame)

        self.titleEntry = ttk.Entry(self.detailFrame, textvariable=self.titleVar, width=30)
        self.titleEntry.grid(row=0, column=1,padx=5 ,pady=5)
        self.authorEntry = ttk.Entry(self.detailFrame, textvariable=self.authorVar, width=30)
        self.authorEntry.grid(row=0, column=3, padx=5 ,pady=5)
        self.yearEntry = ttk.Entry(self.detailFrame, textvariable=self.yearVar, width=30)
        self.yearEntry.grid(row=1, column=1, padx=5 ,pady=5)
        self.isbnEntry = ttk.Entry(self.detailFrame, textvariable=self.isbnVar, width=30)
        self.isbnEntry.grid(row=1, column=3, padx=5 ,pady=5)

        # Create control buttons, parent: controlFrame
        self.viewBtn = ttk.Button(self.controlFrame, text='ViewcAll', command=self.view_all).pack()
        self.searchBtn = ttk.Button(self.controlFrame, text='Search', command=self.search_book).pack()
        self.addBtn = ttk.Button(self.controlFrame, text='Add', command=self.add_entry).pack()
        self.updateBtn = ttk.Button(self.controlFrame, text='Update', command=self.update_entry).pack()
        self.deleteBtn = ttk.Button(self.controlFrame, text='Delete', command=self.delete_entry).pack()
        self.closeBtn = ttk.Button(self.controlFrame, text='Close', command= quit).pack()
        
        for btn in self.controlFrame.pack_slaves():
            btn.pack_configure(padx= 10, pady=6)

        # Create SmartStore database if it doesn't exists.
        db.create_table()

    # Event handling when row is clicked
    def get_selected_row(self, event):
        self.index = self.viewEntryList.curselection()[0]
        self.selectedrow = self.viewEntryList.get(self.index)
        self.details = self.selectedrow.split(',')
        self.selection = self.details[-1].lstrip()
        if self.selection != '':
            selectedBook = db.search_by_isbn(self.selection)
            for book in selectedBook:
                self.titleVar.set(book[0])
                self.authorVar.set(book[1])
                self.yearVar.set(int(book[2]))
                self.isbnVar.set(book[3])

    # Clear all the text inside the entries when adding new entry or deleting existing entry.
    def clear_entries(self):
        self.titleEntry.delete(0, END)
        self.authorEntry.delete(0, END)
        self.yearEntry.delete(0, END)
        self.isbnEntry.delete(0, END)

    # Add a new book     
    def add_entry(self):
        # validate the entries
        self.title = self.titleEntry.get() 
        self.isbn = self.isbnEntry.get()
        self.author = self.authorEntry.get()
        self.year = self.yearEntry.get()
        if self.author == '':
            self.author = 'unknown'
        if self.year==0 or self.year == None:
            self.year = 0
        if self.title == '':
            messagebox.askokcancel(title='Deleting info' , message='Please enter book\'s title')
        elif self.isbn == '':
            messagebox.askokcancel(title='Deleting info' , message='Please enter book\'s isbn')

        if self.title != '' and self.isbn != '':
            # add to the database
            db.insert_entry(self.title, self.author, self.year, self.isbn)
            self.clear_entries()
       
        # checking if the entry successful
        books = db.view_data()
        self.view_books(books)

    # Delete the book based on the details that are given
    def delete_entry(self):
        self.title = self.titleEntry.get()
        self.author = self.authorEntry.get()
        self.isbn = self.isbnEntry.get()
        
        if self.title != '':
            if len(db.search_by_title(self.title)) == 0:
                messagebox.showinfo(title='Deleting Info', message=f'{self.title} does not exists.')
            else:    
                db.delete_title(self.title)
                messagebox.showinfo(title='Deleting Info', message=f'{self.title} has been deleted.')
            self.clear_entries()
        elif self.author != '':
            if len(db.search_by_author(self.author)) == 0:
                messagebox.showinfo(title='Deleting Info', message=f'{self.author} does not exists.')
            else: 
                db.delete_author(self.author)
                messagebox.showinfo(title='Deleting Info', message=f'{self.author} has been deleted.')
            self.clear_entries()
        elif self.isbn != '':
            if len(db.search_by_isbn(self.isbn)) == 0:
                messagebox.showinfo(title='Deleting Info', message=f'{self.isbn} does not exists.')
            else: 
                db.delete_isbn(self.isbn)
                messagebox.showinfo(title='Deleting Info', message=f'{self.isbn} has been deleted.')
            self.clear_entries()
        elif self.selection != '':
            if len(db.search_by_isbn(self.selection)) == 0:
                messagebox.showinfo(title='Deleting Info', message=f'{self.selection} does not exists.')
            else: 
                db.delete_isbn(self.selection)
                messagebox.showinfo(title='Deleting Info', message=f'{self.selection} has been deleted.')
            self.clear_entries()   
        else:
            messagebox.askokcancel(title='Deleting info' , message='Please enter book\'s title or author or ISBN no.')

        # checking if the entry successful
        books = db.view_data()
        self.view_books(books)

    # Search a book based on title or author or year or isbn
    def search_book(self):
        self.title = self.titleEntry.get()
        self.author = self.authorEntry.get()
        self.year = self.yearEntry.get()
        self.isbn = self.isbnEntry.get()
        if self.title !='':
            booksfound = db.search_by_title(self.title)
            self.view_books(booksfound)
        elif self.author !='':
            booksfound = db.search_by_author(self.author)
            self.view_books(booksfound)
        elif self.year !='':
            booksfound = db.search_by_year(self.year)
            self.view_books(booksfound)    
        elif self.isbn !='':
            booksfound = db.search_by_isbn(self.isbn)
            self.view_books(booksfound)

        if self.title == '' and self.author == '' and self.isbn == '':
            messagebox.askokcancel(title='Deleting info' , message='Please enter book\'s title or author or year or ISBN no.')

    # Update book's detail
    def update_entry(self):
        self.title = self.titleEntry.get()
        self.author = self.authorEntry.get()
        self.year = self.yearEntry.get()
        self.isbn = self.isbnEntry.get()
        if self.title == '':
            messagebox.askokcancel(title='Updating info' , message='Please enter book\'s title')
        elif self.isbn == '':
            messagebox.askokcancel(title='updating info' , message='ISBN cannot be empty.')
        if self.author == '':
            self.author = 'unknown'
        if self.year==0 or self.year == None:
            self.year = 0

        if self.title != '' and self.isbn != '':
            # check if the book is exixts or not in database based on ISBN
            findBook = db.search_by_isbn(self.isbn)
            if len(findBook) == 0:
                messagebox.askokcancel(title='updating info' , message='ISBN cannot be found. Do not update the ISBN.')
            else:    
                # add to the database
                db.update_data(self.title, self.author, self.year, self.isbn)
                self.clear_entries()
       
        # view the updated entry
        books = db.view_data()
        self.view_books(books)

    # show book's details in the database into booklist
    def view_books(self, books):
        self.viewEntryList.delete(0, END)
        i = 1 
        for book in books:
            bookdetails =f"{i}. "+ book[0] + ", "+ book[1]+ ", "+ str(book[2])+ ", "+ book[3]
            self.viewEntryList.insert(END, bookdetails)
            i += 1

    # view all the books that available in the database
    def view_all(self):
        books = db.view_data()
        self.view_books(books)        

def main():
    root = Tk()
    app = BookStore(root)
    root.mainloop()
    
if __name__== '__main__': main()    