# Project 6 ~ Task and Productivity Manager

import json
import os
from datetime import datetime

FILE = "tasks.json"

# function to load tasks
def load_tasks():
    # checking if file exists
    if os.path.exists(FILE):
        try:
            f = open(FILE, "r")
            data = json.load(f)
            f.close()
            return data
        except:
            print("File is empty or broken, starting new")
            return []
    else:
        return []

# saving function
def save_tasks(tasks):
    f = open(FILE, "w")
    json.dump(tasks, f)
    f.close()
    

def add_task(tasks):
    print("-- ADD TASK ---")
    title = input("Enter title: ")
    if title == "":
        print("Title cant be empty")
        return
    
    desc = input("Enter description: ")
    due = input("Enter due date (YYYY-MM-DD): ")

    # checking the date
    try:
        datetime.strptime(due, "%Y-%m-%d")
    except:
        print("Wrong date format! Please use YYYY-MM-DD")
        return

    print("Priority: High, Medium, Low")
    priority = input("Enter priority: ")

  
    priority = priority.capitalize()
    if priority != "High" and priority != "Medium" and priority != "Low":
        print("Invalid priority, setting to Low")
        priority = "Low"

    # finding the new id
    new_id = 1
    for t in tasks:
        if t["id"] >= new_id:
            new_id = t["id"] + 1

    # the task dictionary
  
    new_task = {}
    new_task["id"] = new_id
    new_task["title"] = title
    new_task["description"] = desc
    new_task["due_date"] = due
    new_task["priority"] = priority
    new_task["status"] = "Pending"

    tasks.append(new_task)
    save_tasks(tasks)
    print("Task is added! naiss!")

def view_all(tasks):
    if len(tasks) == 0:
        print("No tasks yet. Add some!")
        return

    print("--- ALL MY TASKS ---")
    # first show High priority
    for p in ["High", "Medium", "Low"]:
        for t in tasks:
            if t["priority"] == p:
                print("")
                print(f"ID: {t['id']}")
                print(f"Title: {t['title']}")
                print(f"Desc: {t['description']}")
                print(f"Due: {t['due_date']}")
                print(f"Priority: {t['priority']}")
                print(f"Status: {t['status']}")
                
                # check overdue
                today = datetime.now().date()
                due_date = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
                if due_date < today and t["status"] == "Pending":
                    print("> THIS IS OVERDUE!!! <")

def view_pending(tasks):
    print("--- PENDING TASKS ---")
    found = False
    for t in tasks:
        if t["status"] == "Pending":
            found = True
            print(f"ID:{t['id']} | {t['title']} | Due:{t['due_date']} | {t['priority']}")
    if found == False:
        print("No pending tasks")

def view_completed(tasks):
    print("--- COMPLETED TASKS ---")
    found = False
    for t in tasks:
        if t["status"] == "Completed":
            found = True
            print(f"ID:{t['id']} | {t['title']} | Due:{t['due_date']}")
    if found == False:
        print("No completed tasks")

def complete_task(tasks):
    view_all(tasks)
    id_str = input("Enter ID to complete: ")
    if id_str.isdigit() == False:
        print("Please enter number")
        return
    my_id = int(id_str)
    for t in tasks:
        if t["id"] == my_id:
            t["status"] = "Completed"
            save_tasks(tasks)
            print(f"Task {my_id} completed! Nice work!")
            return
    print("ID not found")

def delete_task(tasks):
    view_all(tasks)
    id_str = input("\nEnter ID to delete: ")
    if not id_str.isdigit():
        print("Enter number only")
        return
    my_id = int(id_str)
    i = 0
    while i < len(tasks):
        if tasks[i]["id"] == my_id:
            tasks.pop(i)
            save_tasks(tasks)
            print("Deleted!")
            return
        i = i + 1
    print("Not found,sorryy")

def search_task(tasks):
    word = input("\n Search word: ")
    word = word.lower()
    print(f"\n Searching for {word}...")
    found = False
    for t in tasks:
        if word in t["title"].lower() or word in t["description"].lower():
            found = True
            print(f"Found - ID:{t['id']} Title:{t['title']} Status:{t['status']}")
    if found == False:
        print("Nothing found")

def update_task(tasks):
    view_all(tasks)
    id_str = input("\nEnter ID to update: ")
    if not id_str.isdigit():
        print("Bad ID")
        return
    my_id = int(id_str)
    for t in tasks:
        if t["id"] == my_id:
            print(f"Updating {t['title']}")
            new_title = input("New title (press enter to keep old): ")
            if new_title != "":
                t["title"] = new_title
            new_desc = input("New description (enter to keep): ")
            if new_desc != "":
                t["description"] = new_desc
            save_tasks(tasks)
            print("Updated!")
            return
    print("ID not found")

# main program 
def main():
    
    print("  THE TASK MANAGER - PROJECT 6")
    
    print("Welcome! This program helps manage tasks")

    tasks = load_tasks()
    print(f"Loaded {len(tasks)} tasks from the file")

    while True:
        print("---------------- MENU --------")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Pending")
        print("4. View Completed")
        print("5. Complete a Task")
        print("6. Update Task")
        print("7. Delete Task")
        print("8. Search")
        print("9. Exit")
        print("-------------------")

        # 
        total = len(tasks)
        pending = 0
        comp = 0
        for t in tasks:
            if t["status"] == "Pending":
                pending = pending + 1
            else:
                comp = comp + 1
        print(f"Total:{total} Pending:{pending} Completed:{comp}")

        choice = input("\nEnter your choice (1-9): ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_all(tasks)
        elif choice == "3":
            view_pending(tasks)
        elif choice == "4":
            view_completed(tasks)
        elif choice == "5":
            complete_task(tasks)
        elif choice == "6":
            update_task(tasks)
        elif choice == "7":
            delete_task(tasks)
        elif choice == "8":
            search_task(tasks)
        elif choice == "9":
            print("Byeeeeee! Saving...")
            save_tasks(tasks)
            break
        else:
            print("Wrong choice! Try again 1-9")

#running the program
main()