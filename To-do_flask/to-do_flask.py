import os
import json
from flask import Flask, render_template, request, redirect, url_for
import secrets
import string

# Initialize Flask app
app = Flask(__name__)

# Define absolute path for storing the to-do list JSON file
DATA_FILE = os.path.join(app.root_path, 'todo.json')


def generate_unique_id(existing_ids, length=6):
    """
    Generate a unique alphanumeric ID that is not in existing_ids.

    Args:
        existing_ids (set): Set of IDs that already exist.
        length (int): Length of the generated ID (default: 6).

    Returns:
        str: A unique alphanumeric ID.
    """
    alphabet = string.ascii_letters + string.digits
    while True:
        new_id = ''.join(secrets.choice(alphabet) for _ in range(length))
        if new_id not in existing_ids:
            return new_id


def load_list():
    """
    Load the to-do list from the JSON file.

    - Creates an empty list if the file does not exist.
    - Ensures all tasks have unique IDs.
    - Updates the file if missing IDs are added.

    Returns:
        list: A list of tasks, where each task is a dictionary.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, 'r') as f:
            todo = json.load(f)
    except json.JSONDecodeError:
        # If the file is corrupted or empty, return an empty list
        return []

    # Collect existing IDs
    existing_ids = {task.get('id') for task in todo if task.get('id')}
    updated = False

    # Ensure every task has an ID
    for task in todo:
        if 'id' not in task or not task['id']:
            task['id'] = generate_unique_id(existing_ids)
            existing_ids.add(task['id'])
            updated = True

    # Save updated list if changes were made
    if updated:
        save_list(todo)

    return todo


def save_list(todo):
    """
    Save the to-do list to the JSON file.

    Args:
        todo (list): The to-do list to save.
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(todo, f, indent=4)


@app.route('/add_task', methods=['POST'])
def add_task():
    """
    Route: /add_task
    Method: POST

    Add a new task to the to-do list with unique ID, task name,
    status, and priority. Saves the updated list and redirects
    back to the main to-do list page.
    """
    todo = load_list()
    existing_ids = {task.get('id') for task in todo}

    # Create a new task dictionary
    new_task = {
        'id': generate_unique_id(existing_ids),
        'task': request.form['task'],
        'status': request.form['status'],
        'priority': request.form['priority']
    }

    # Append and save
    todo.append(new_task)
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    """
    Route: /edit_task/<task_id>
    Method: POST

    Edit an existing task in the to-do list by task ID.
    Updates task details (task name, status, priority),
    then saves and redirects to the main to-do page.

    Args:
        task_id (str): The unique ID of the task to edit.
    """
    todo = load_list()
    for task in todo:
        if task['id'] == task_id:
            task['task'] = request.form['task']
            task['status'] = request.form['status']
            task['priority'] = request.form['priority']
            break
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Route: /delete_task/<task_id>
    Method: POST

    Delete a task from the to-do list by task ID.
    Saves the updated list and redirects back
    to the main to-do page.

    Args:
        task_id (str): The unique ID of the task to delete.
    """
    todo = load_list()
    # Keep all tasks except the one with the matching ID
    todo = [task for task in todo if task['id'] != task_id]
    save_list(todo)
    return redirect(url_for('show_todo'))


@app.route('/')
def show_todo():
    """
    Route: /
    Method: GET

    Load the to-do list and render the index.html template
    to display tasks to the user.
    """
    todo_list = load_list()
    return render_template('index.html', todo=todo_list)


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
