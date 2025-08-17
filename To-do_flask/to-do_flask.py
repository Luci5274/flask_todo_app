from flask import Flask, render_template, request,redirect,url_for
import json

app = Flask(__name__)

#One function for loading the JSON file
def load_list():
    with open('todo.json', 'r') as f:
        return json.load(f)

def save_list(todo):
    with open('todo.json', 'w') as f:
        json.dump(todo, f, indent=4)

@app.route('/add_task',methods=['POST'])
def add_task():
    todo = load_list()
    new_task = {
        'task':request.form['task'],
        'status': request.form['status'],
        'priority': request.form['priority']
    }
    todo.append(new_task)
    save_list(todo)
    return redirect(url_for('show_todo'))

#Keep a single route for '/'
# Removed the duplicate and corrected the missing @ decorator
@app.route('/')
def show_todo():
    # Load the tasks from the JSON file
    todo_list = load_list()

    # Pass them into the template as "todo"
    # Changed template to "index.html" to follow Flask convention
    return render_template('index.html', todo=todo_list)

if __name__ == '__main__':
    app.run(debug=True)
