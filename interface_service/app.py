from flask import Flask, jsonify, render_template, request
import redis
import threading
import requests

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
# ganti dengan ip kamu
url = 'http://192.168.0.7:5000' 

tasks = []

def event_listener():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('task_channel')
    for message in pubsub.listen():
        if message['type'] == 'message':
            task_message = message['data'].decode('utf-8')
            if 'New task added' in task_message:
                task = task_message.replace('New task added: ', '')
                tasks.append(task)
            elif 'Task deleted' in task_message:
                task = task_message.replace('Task deleted: ', '')
                if task in tasks:
                    tasks.remove(task)
            print(f"Received message: {task_message}")

listener_thread = threading.Thread(target=event_listener)
listener_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add_task_form():
    return render_template('add.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    response = requests.post(f'{url}/tasks', json={"task": task})
    if response.status_code == 201:
        message = 'Task added successfully!'
    else:
        message = 'Failed to add task'
    return render_template('add.html', message=message)

@app.route('/delete_task', methods=['DELETE'])
def delete_task():
    task = request.json.get('task')
    response = requests.delete(f'{url}/tasks', json={"task": task})
    if response.status_code == 200:
        return jsonify({"message": "Task deleted"}), 200
    else:
        return jsonify({"error": "Failed to delete task"}), response.status_code

@app.route('/tasks', methods=['GET'])
def get_tasks():
    response = requests.get(f'{url}/tasks')
    if response.status_code == 200:
        tasks_from_service = response.json()
        # Update local tasks list
        global tasks
        tasks = tasks_from_service
        return jsonify(tasks_from_service), 200
    return jsonify({"error": "Failed to fetch tasks"}), response.status_code

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "Interface Service is running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
