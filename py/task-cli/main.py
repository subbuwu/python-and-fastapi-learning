#!/usr/bin/env python3
import sys
import json
from datetime import datetime


FILE_NAME = "./data.json"


# Create data.json if it doesn't exist
try:
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    data = []


if len(sys.argv) < 2:
    print("Please provide a command.")
    sys.exit()


task_type = sys.argv[1]


# ADD
if task_type == "add":

    if len(sys.argv) < 3:
        print("Please provide a task description.")
        sys.exit()

    task_content = sys.argv[2]

    if len(data) == 0:
        next_id = 1
    else:
        next_id = max(task["id"] for task in data) + 1

    current_time = datetime.now().isoformat()

    data.append(
        {
            "id": next_id,
            "description": task_content,
            "status": "todo",
            "createdAt": current_time,
            "updatedAt": current_time,
        }
    )

    print(f"Task added successfully (ID: {next_id})")


# UPDATE
elif task_type == "update":

    if len(sys.argv) < 4:
        print("Usage: update <id> <description>")
        sys.exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit()

    task_update_content = sys.argv[3]

    task_found = False

    for task in data:
        if task["id"] == task_id:
            task["description"] = task_update_content
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if not task_found:
        print(f"Task with ID {task_id} not found.")


# DELETE
elif task_type == "delete":

    if len(sys.argv) < 3:
        print("Usage: delete <id>")
        sys.exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit()

    task_found = False

    for task in data:
        if task["id"] == task_id:
            data.remove(task)
            task_found = True
            break

    if not task_found:
        print(f"Task with ID {task_id} not found.")


# MARK IN PROGRESS
elif task_type == "mark-in-progress":

    if len(sys.argv) < 3:
        print("Usage: mark-in-progress <id>")
        sys.exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit()

    task_found = False

    for task in data:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if not task_found:
        print(f"Task with ID {task_id} not found.")


# MARK DONE
elif task_type == "mark-done":

    if len(sys.argv) < 3:
        print("Usage: mark-done <id>")
        sys.exit()

    try:
        task_id = int(sys.argv[2])
    except ValueError:
        print("Task ID must be a number.")
        sys.exit()

    task_found = False

    for task in data:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if not task_found:
        print(f"Task with ID {task_id} not found.")


# LIST
elif task_type == "list":

    if len(sys.argv) == 2:
        # List all tasks
        for task in data:
            print(task)

    else:
        status = sys.argv[2]

        if status not in ["done", "todo", "in-progress"]:
            print("Invalid status.")
            sys.exit()

        for task in data:
            if task["status"] == status:
                print(task)


# INVALID COMMAND
else:
    print(f"Unknown command: {task_type}")
    sys.exit()


# Save changes to JSON
if task_type in [
    "add",
    "update",
    "delete",
    "mark-in-progress",
    "mark-done",
]:
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)