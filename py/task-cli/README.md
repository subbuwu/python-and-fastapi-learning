# Task Tracker CLI

A simple command-line task tracker built with Python. Tasks are stored locally in a JSON file.

## Features

* Add, update, and delete tasks
* Mark tasks as `todo`, `in-progress`, or `done`
* List all tasks or filter by status
* Stores tasks in `data.json`

## Usage

```bash
task-cli add "Buy groceries"
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

task-cli mark-in-progress 1
task-cli mark-done 1

task-cli list
task-cli list todo
task-cli list in-progress
task-cli list done
```

## Source

[GitHub Repository](https://github.com/subbuwu/python-and-fastapi-learning/tree/main/py/task-cli)
