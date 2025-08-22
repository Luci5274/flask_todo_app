import os
import json
from flask import Flask, render_template, request, redirect, url_for
from uuid import uuid4

app = Flask(__name__)

DATA_FILE = 'todo.json'

def load_list():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_list(todo):
    with open(DATA_FILE, 'w') as f:
        json.dump(todo, f, indent=4)

@app.route('/add_task', methods=['POST'])
def add_task():
    todo = load_list()
    new_task = {
        'id': str(uuid4()),
        'task': request.form['task'],
        'status': request.form['status'],
        'priority': request.form['priority']
    }
    todo.append(new_task)
    save_list(todo)
    return redirect(url_for('show_todo'))

@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
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
    todo = load_list()
    todo = [task for task in todo if task['id'] != task_id]
    save_list(todo)
    return redirect(url_for('show_todo'))

@app.route('/')
def show_todo():
    todo_list = load_list()
    return render_template('index.html', todo=todo_list)

if __name__ == '__main__':
    app.run(debug=True)
