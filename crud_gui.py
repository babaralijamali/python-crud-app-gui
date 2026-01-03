import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- Database Setup ---
conn = sqlite3.connect("crud_gui.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
""")
conn.commit()

# --- Functions ---
def refresh_tree():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM users")
    for user in cursor.fetchall():
        tree.insert("", tk.END, values=user)

def add_user():
    name = name_var.get()
    email = email_var.get()
    if name and email:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        refresh_tree()
        name_var.set("")
        email_var.set("")
    else:
        messagebox.showwarning("Input Error", "Name and Email cannot be empty")

def update_user():
    try:
        selected_item = tree.selection()[0]
        user_id = tree.item(selected_item)["values"][0]
        name = name_var.get()
        email = email_var.get()
        cursor.execute("UPDATE users SET name=?, email=? WHERE id=?", (name, email, user_id))
        conn.commit()
        refresh_tree()
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a user to update")

def delete_user():
    try:
        selected_item = tree.selection()[0]
        user_id = tree.item(selected_item)["values"][0]
        cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        refresh_tree()
    except IndexError:
        messagebox.showwarning("Selection Error", "Select a user to delete")

def select_user(event):
    try:
        selected_item = tree.selection()[0]
        user = tree.item(selected_item)["values"]
        name_var.set(user[1])
        email_var.set(user[2])
    except IndexError:
        pass

# --- GUI Setup ---
root = tk.Tk()
root.title("Python CRUD GUI App")

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5)
tk.Label(frame, text="Email:").grid(row=1, column=0, padx=5)

name_var = tk.StringVar()
email_var = tk.StringVar()

tk.Entry(frame, textvariable=name_var).grid(row=0, column=1, padx=5)
tk.Entry(frame, textvariable=email_var).grid(row=1, column=1, padx=5)

tk.Button(frame, text="Add", command=add_user, bg="green", fg="white").grid(row=0, column=2, padx=5)
tk.Button(frame, text="Update", command=update_user, bg="blue", fg="white").grid(row=1, column=2, padx=5)
tk.Button(frame, text="Delete", command=delete_user, bg="red", fg="white").grid(row=2, column=2, padx=5)

# Treeview for users
tree = ttk.Treeview(root, columns=("ID", "Name", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.pack(pady=10)

tree.bind("<<TreeviewSelect>>", select_user)

refresh_tree()
root.mainloop()
conn.close()
