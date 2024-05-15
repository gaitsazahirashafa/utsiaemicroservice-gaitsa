document.addEventListener('DOMContentLoaded', function () {
    function fetchTasks() {
        fetch('/tasks')
            .then(response => response.json())
            .then(data => {
                const taskList = document.getElementById('tasks');
                taskList.innerHTML = '';
                data.forEach(task => {
                    const li = document.createElement('li');
                    li.textContent = task;

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.addEventListener('click', function () {
                        let newTask = handleNewMessage(task);
                        deleteTask(newTask)

                    });

                    li.appendChild(deleteButton);
                    taskList.appendChild(li);
                });
            });
    }

    function handleNewMessage(message) {
        const task = message.replace('New task added: ', '');
        return task;
    }

    function deleteTask(task) {

        console.log(task)

        fetch('/delete_task', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: task })
        }).then(response => {
            if (response.status === 200) {
                fetchTasks();
            } else {
                alert('Failed to delete task');
            }
        });
    }

    fetchTasks();
    setInterval(fetchTasks, 5000);  // Update every 5 seconds
});
