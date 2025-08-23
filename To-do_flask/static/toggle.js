document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('toggle-add-task');
    const addTaskForm  = document.getElementById('add-task-form');
    const taskList     = document.getElementById('task-list');

    // Toggle Add Task form
    if (toggleButton && addTaskForm) {
        toggleButton.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent bubbling messing with li toggles
            addTaskForm.classList.toggle('hidden');
        });
    }

    // Toggle the per-task edit/delete form by clicking on the li
    if (taskList) {
        taskList.addEventListener('click', (event) => {
            const li = event.target.closest('li');
            if (!li) return;

            // If the user clicked inside a form (edit/delete), do nothing
            if (event.target.closest('.task-form')) return;

            const form = li.querySelector('.task-form');
            if (form) {
                form.classList.toggle('hidden');
            }
        });
    }
});