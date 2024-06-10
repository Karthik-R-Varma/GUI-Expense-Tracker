import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store expenses
EXPENSES_FILE = 'expenses.json'

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'r') as file:
            return json.load(file)
    return []

def save_expenses(expenses):
    with open(EXPENSES_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

def add_expense(expenses, name, amount):
    expenses.append({"name": name, "amount": amount})
    save_expenses(expenses)
    update_expense_list(expenses)

def delete_expense(expenses, idx):
    if 0 <= idx < len(expenses):
        removed_expense = expenses.pop(idx)
        save_expenses(expenses)
        update_expense_list(expenses)
        messagebox.showinfo("Success", f"Deleted expense: {removed_expense['name']}, Amount: {removed_expense['amount']}")
    else:
        messagebox.showerror("Error", "Invalid expense number.")

def update_expense_list(expenses):
    listbox.delete(0, tk.END)
    total = 0
    for idx, expense in enumerate(expenses, start=1):
        listbox.insert(tk.END, f"{idx}. {expense['name']} - ${expense['amount']:.2f}")
        total += expense['amount']
    total_label.config(text=f"Total amount spent: ${total:.2f}")

def on_add_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    if name and amount:
        try:
            amount = float(amount)
            add_expense(expenses, name, amount)
            name_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    else:
        messagebox.showerror("Error", "Please enter both name and amount.")

def on_delete_expense():
    try:
        idx = int(delete_entry.get()) - 1
        delete_expense(expenses, idx)
        delete_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid expense number.")

expenses = load_expenses()

# Create the main window
root = tk.Tk()
root.title("Expense Tracker")

# Create and place widgets
tk.Label(root, text="Expense Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Expense Amount:").grid(row=1, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Expense", command=on_add_expense)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

total_label = tk.Label(root, text="Total amount spent: $0.00")
total_label.grid(row=4, column=0, columnspan=2, pady=5)

tk.Label(root, text="Expense Number to Delete:").grid(row=5, column=0, padx=10, pady=5)
delete_entry = tk.Entry(root)
delete_entry.grid(row=5, column=1, padx=10, pady=5)

delete_button = tk.Button(root, text="Delete Expense", command=on_delete_expense)
delete_button.grid(row=6, column=0, columnspan=2, pady=10)

update_expense_list(expenses)

# Start the main event loop
root.mainloop()
