document.addEventListener('DOMContentLoaded', () => {
    // Grab the toggle button, form, and task list
    const toggleButton = document.getElementById('toggle-add-task');
    const addTaskForm = document.getElementById('add-task-form');
    const taskList = document.getElementById('task-list');

    // Add click event listener to the toggle button
    toggleButton.addEventListener('click', () => {
        addTaskForm.classList.toggle('hidden');
    });

    // Detect clicks on task text → toggle its form
    if (taskList) {
        taskList.addEventListener('click', (event) => {
            const li = event.target.closest('li');
            if (li && event.target.classList.contains('task-text')) {
                const form = li.querySelector('.task-form');
                if (form) form.classList.toggle('hidden');
            }
        });
    }
});
