from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

todolist = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(todolist), 200

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        todolist.append(task)
        redis_client.publish('task_channel', f'New task added: {task}')
        return jsonify({"message": "Task added"}), 201
    return jsonify({"error": "Task is required"}), 400

@app.route('/tasks', methods=['DELETE'])
def delete_task():
    task = request.json.get('task')
    if task in todolist:
        todolist.remove(task)
        redis_client.publish('task_channel', f'Task deleted: {task}')
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
