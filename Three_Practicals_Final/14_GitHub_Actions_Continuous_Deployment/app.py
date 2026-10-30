from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Complete Docker practical", "done": False},
    {"id": 2, "title": "Submit GitHub assignment", "done": True},
]
next_id = 3

PAGE = """
<!doctype html>
<html><head><title>To-Do App</title>
<style>
body{font-family:Arial;max-width:650px;margin:45px auto;padding:0 18px;background:#f5f7fb}
h1{color:#26344a}.box{background:white;padding:22px;border-radius:12px;box-shadow:0 2px 12px #ddd}
input{padding:10px;width:65%}button{padding:10px 14px;cursor:pointer}
li{margin:12px 0}.done{text-decoration:line-through;color:gray}
small{color:#64748b}
</style></head><body><div class="box">
<h1>My To-Do List</h1><p>Flask application running in a Docker container.</p>
<form method="post" action="/add"><input name="title" placeholder="Enter a task" required><button>Add task</button></form>
<ul>{% for task in tasks %}
<li><span class="{{ 'done' if task.done else '' }}">{{ task.title }}</span>
<form style="display:inline" method="post" action="/toggle/{{task.id}}"><button>Toggle</button></form>
<form style="display:inline" method="post" action="/delete/{{task.id}}"><button>Delete</button></form></li>
{% endfor %}</ul><small>Health endpoint: /health | JSON API: /api/tasks</small>
</div></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE, tasks=tasks)

@app.get("/health")
def health():
    return jsonify(status="healthy")

@app.get("/api/tasks")
def get_tasks():
    return jsonify(tasks)

@app.post("/api/tasks")
def create_task():
    global next_id
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = {"id": next_id, "title": title, "done": False}
    next_id += 1
    tasks.append(task)
    return jsonify(task), 201

@app.post("/add")
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({"id": next_id, "title": title, "done": False})
        next_id += 1
    return home()

@app.post("/toggle/<int:task_id>")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return home()

@app.post("/delete/<int:task_id>")
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return home()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
