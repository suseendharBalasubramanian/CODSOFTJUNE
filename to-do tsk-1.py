import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# Function to load tasks from a JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save tasks to a JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Function to display tasks
def display_tasks(category=None):
    tasks_tree.delete(*tasks_tree.get_children())  # Clear existing tasks

    tasks_to_display = tasks if category is None else [task for task in tasks if task.get('category') == category]
    
    for index, task in enumerate(sorted(tasks_to_display, key=lambda x: x['due_date']), start=1):
        status = "Done" if task['done'] else "Not Done"
        tasks_tree.insert('', 'end', values=(index, task['title'], task['description'], task['due_date'], status, task.get('category', 'Uncategorized')))

# Function to add a new task
def add_task():
    title = title_entry.get()
    description = description_entry.get()
    due_date = due_date_entry.get()

    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        result_label.config(text="Invalid date format. Use YYYY-MM-DD.")
        return

    category = category_entry.get()

    tasks.append({"title": title, "description": description, "due_date": due_date, "done": False, "category": category})
    save_tasks(tasks)
    result_label.config(text="Task added successfully!")
    clear_entries()
    display_tasks()

# Function to clear input entries
def clear_entries():
    title_entry.delete(0, 'end')
    description_entry.delete(0, 'end')
    due_date_entry.delete(0, 'end')
    category_entry.delete(0, 'end')

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Create and set up the notebook (tabs for different functions)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create a tab for displaying tasks
display_tab = ttk.Frame(notebook)
notebook.add(display_tab, text='Display Tasks')

# Create a tab for adding tasks
add_tab = ttk.Frame(notebook)
notebook.add(add_tab, text='Add Task')

# Add widgets to the "Display Tasks" tab
category_label = ttk.Label(display_tab, text="Filter by Category:")
category_label.pack(pady=10)

category_var = tk.StringVar()
category_entry = ttk.Entry(display_tab, textvariable=category_var)
category_entry.pack()

display_button = ttk.Button(display_tab, text="Display", command=lambda: display_tasks(category_var.get()))
display_button.pack()

tasks_tree = ttk.Treeview(display_tab, columns=('Index', 'Title', 'Description', 'Due Date', 'Status', 'Category'))
tasks_tree.heading('#1', text='Index')
tasks_tree.heading('#2', text='Title')
tasks_tree.heading('#3', text='Description')
tasks_tree.heading('#4', text='Due Date')
tasks_tree.heading('#5', text='Status')
tasks_tree.heading('#6', text='Category')
tasks_tree.pack(padx=10, pady=10)

# Add widgets to the "Add Task" tab
title_label = ttk.Label(add_tab, text="Title:")
title_label.pack(pady=5)

title_var = tk.StringVar()
title_entry = ttk.Entry(add_tab, textvariable=title_var)
title_entry.pack()

description_label = ttk.Label(add_tab, text="Description:")
description_label.pack(pady=5)

description_var = tk.StringVar()
description_entry = ttk.Entry(add_tab, textvariable=description_var)
description_entry.pack()

due_date_label = ttk.Label(add_tab, text="Due Date (YYYY-MM-DD):")
due_date_label.pack(pady=5)

due_date_var = tk.StringVar()
due_date_entry = ttk.Entry(add_tab, textvariable=due_date_var)
due_date_entry.pack()

category_label = ttk.Label(add_tab, text="Category (optional):")
category_label.pack(pady=5)

category_var = tk.StringVar()
category_entry = ttk.Entry(add_tab, textvariable=category_var)
category_entry.pack()

add_button = ttk.Button(add_tab, text="Add Task", command=add_task)
add_button.pack(pady=10)

result_label = ttk.Label(add_tab, text="")
result_label.pack()

# Initialize tasks
tasks = load_tasks()

# Display tasks on the initial load
display_tasks()

# Start the GUI main loop
root.mainloop()
