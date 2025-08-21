document.addEventListener('DOMContentLoaded', () => {
    // Grab the toggle button and the form
    const toggleButton = document.getElementById('toggle-add-task');
    const addTaskForm = document.getElementById('add-task-form');

    // Add click event listener to the button
    toggleButton.addEventListener('click', () => {
        // Toggle form visibility
        if (addTaskForm.style.display === 'none') {
            addTaskForm.style.display = 'block';
        } else {
            addTaskForm.style.display = 'none';
        }
    });
});