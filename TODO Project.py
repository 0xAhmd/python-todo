# Import the tkinter module, which is used for creating GUI applications
import tkinter
from tkinter import *

# Create the main window of the application
root = Tk()

# Set the title of the window to 'TODO List'
root.title('TODO List')

# Set the dimensions of the window to 300x550 pixels
root.geometry('300x550')

# Make the window non-resizable in both directions
root.resizable(False, False)

Task_list = []
filepath = "tasklist2.txt"  # Path to task file

def opentaskfile():
    try:
        with open(filepath, 'r') as taskfile:
            tasks = taskfile.readlines()
            for task in tasks:
                if task != '\n':
                    Task_list.append(task.strip())
                    listbox.insert(END, task.strip())
    except FileNotFoundError:
        with open(filepath, 'w') as taskfile:
            pass  # Create the file if it does not exist

def addtask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        with open(filepath, 'a') as taskfile:
            taskfile.write(task + '\n')
        Task_list.append(task)
        listbox.insert(END, task)

def deletetask():
    global Task_list
    task = str(listbox.get(ANCHOR))
    if task in Task_list:
        Task_list.remove(task)
        with open(filepath, 'w') as taskfile:
            for task in Task_list:
                taskfile.write(task + '\n')
        listbox.delete(ANCHOR)

def mark_as_completed(event):
    selected_index = listbox.nearest(event.y)
    if selected_index >= 0:
        # Create a context menu
        context_menu = Menu(root, tearoff=0)
        context_menu.add_command(label="Mark as Completed",
                                  command=lambda idx=selected_index: mark_task_completed(idx))
        context_menu.post(event.x_root, event.y_root)

def mark_task_completed(selected_index):
    listbox.itemconfig(selected_index, {'bg': 'green'})

# Heading label
heading = Label(root, text="All Tasks", font="Arial 22 bold", fg="white", bg="#7250bc")
heading.pack(fill=X)

# Input and button frame
frame = Frame(root, width=400, height=50, bg="white")
frame.place(x=0, y=50)

task_entry = Entry(frame, width=18, font="Arial 18", bd=0)
task_entry.place(x=10, y=9)
task_entry.focus()

button = Button(frame, text="ADD", font="Arial 16 bold", width=6, bg="#7250bc", fg="#fff", bd=0, command=addtask)
button.place(x=200, y=5)

# ListBox frame
frame1 = Frame(root, bd=3, width=300, height=280, bg="#7250bc")
frame1.pack(pady=(60, 5))

listbox = Listbox(frame1, font=("Arial", 12), width=30, height=10, bg="#eeeeee", fg="black",
                  selectbackground="#5a95ff")
listbox.pack(side=LEFT, fill=BOTH, padx=2)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Delete Button
delete_button = Button(root, text="Delete Task", font="Arial 14 bold", bg="#ff5c5c", fg="white", bd=0, command=deletetask)
delete_button.pack(side=BOTTOM, pady=13)

# Bind right-click event to mark_as_completed function
listbox.bind("<Button-3>", mark_as_completed)

# Load tasks from file
opentaskfile()

# Run the application
root.mainloop()
