"""
A simple Desktop CRUD Application using Python.
- Frontend: Tkinter (Built-in Python GUI library, similar to Java Swing or AWT)
- Backend Logic & Database: SQLite3 (Built-in lightweight database)

CRUD stands for Create, Read, Update, Delete.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book - Python CRUD")
        self.root.geometry("500x450")
        
        # 1. Initialize our backend (Database)
        self.init_database()
        
        # 2. Build our frontend (UI)
        self.setup_ui()
        
        # 3. Read data from database and populate the table
        self.load_contacts()
        
        self.selected_contact_id = None # Keep track of currently clicked contact

    # ==========================================
    # BACKEND: Database Setup & Connections
    # ==========================================
    def init_database(self):
        """Creates the SQLite database and table if they don't exist."""
        # SQLite creates a local file 'contacts.db' to store data.
        self.conn = sqlite3.connect("contacts.db")
        self.cursor = self.conn.cursor()
        
        # SQL syntax to create a table.
        # AUTOINCREMENT automatically assigns a unique ID to each new row.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    # ==========================================
    # FRONTEND: User Interface Construction
    # ==========================================
    def setup_ui(self):
        """Creates the labels, text boxes, buttons, and the data table."""
        
        # --- Top Frame for Inputs ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10) # pack() is a layout manager, similar to BorderLayout regions

        tk.Label(input_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5) # grid() is like GridLayout in Java

        tk.Label(input_frame, text="Phone:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        # --- Middle Frame for Buttons ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        # The 'command' parameter links the button click to a specific method (like ActionListener)
        tk.Button(btn_frame, text="Add (Create)", command=self.add_contact, bg="green", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_contact, bg="blue", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_contact, bg="red", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_fields).grid(row=0, column=3, padx=5)

        # --- Bottom Frame for Data Table (Treeview) ---
        columns = ("ID", "Name", "Phone")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        
        # Define table headings and column widths
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", width=200, anchor=tk.W)
        
        self.tree.heading("Phone", text="Phone Number")
        self.tree.column("Phone", width=150, anchor=tk.W)
        
        self.tree.pack(pady=10)
        
        # Bind the row selection event so we can click on a row to edit it
        self.tree.bind("<ButtonRelease-1>", self.select_record)


    # ==========================================
    # CRUD OPERATIONS (Connecting Frontend & Backend)
    # ==========================================

    def add_contact(self):
        """CREATE: Grabs data from UI and saves it to DB."""
        # Get data from frontend Text Entries
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if name == "" or phone == "":
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        # Backend SQL Insert
        self.cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
        self.conn.commit()
        
        # Update the UI
        self.clear_fields()
        self.load_contacts()
        messagebox.showinfo("Success", "Contact Added Successfully!")

    def load_contacts(self):
        """READ: Fetches data from DB and updates the UI Table."""
        # Clear existing items in the tree view (Frontend reset)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Backend SQL Select
        self.cursor.execute("SELECT * FROM contacts")
        rows = self.cursor.fetchall() # Returns a list of tuples like [(1, "John", "555-1234"), ...]

        # Populate Frontend Table
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def select_record(self, event):
        """HELPER: Automatically populates textboxes when a user clicks a row."""
        selected_item = self.tree.focus() # Get clicked row
        if not selected_item:
            return
            
        values = self.tree.item(selected_item, "values")
        
        # values[0] is ID, values[1] is Name, values[2] is Phone
        self.selected_contact_id = values[0]
        
        self.clear_fields()
        self.name_entry.insert(0, values[1])
        self.phone_entry.insert(0, values[2])

    def update_contact(self):
        """UPDATE: Merges modified UI input back into DB."""
        if not self.selected_contact_id:
            messagebox.showwarning("Selection Error", "Please select a contact from the list first!")
            return

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if name == "" or phone == "":
            messagebox.showwarning("Input Error", "Please fill in all fields!")
            return

        # Backend SQL Update
        self.cursor.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, self.selected_contact_id))
        self.conn.commit()

        # Update UI
        self.clear_fields()
        self.load_contacts()
        self.selected_contact_id = None
        messagebox.showinfo("Success", "Contact Updated Successfully!")

    def delete_contact(self):
        """DELETE: Removes selected contact from DB."""
        if not self.selected_contact_id:
            messagebox.showwarning("Selection Error", "Please select a contact from the list first!")
            return

        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            # Backend SQL Delete
            self.cursor.execute("DELETE FROM contacts WHERE id=?", (self.selected_contact_id,))
            self.conn.commit()

            # Update UI
            self.clear_fields()
            self.load_contacts()
            self.selected_contact_id = None
            messagebox.showinfo("Success", "Contact Deleted Successfully!")

    def clear_fields(self):
        """HELPER: Empties the input text boxes."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)


# Start the Application
if __name__ == "__main__":
    # In Tkinter, you must initialize the main root window first
    root = tk.Tk()
    
    # Create an instance of our application class
    app = ContactBookApp(root)
    
    # Start the GUI event loop (similar to waiting for events in Java Swing)
    root.mainloop()
