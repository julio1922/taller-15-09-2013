from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configura la cadena de conexión a la base de datos Access
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\cuc\Documents\TasksDB.accdb;"
)

# Establece una conexión a la base de datos
connection = pyodbc.connect(conn_str)

# Define el cursor para ejecutar consultas SQL
cursor = connection.cursor()

# Ruta para mostrar todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    task_list = []
    for task in tasks:
        task_dict = {
            'id': task[0],
            'title': task[1],
            'completed': task[2]
        }
        task_list.append(task_dict)
    return jsonify(task_list)

# Ruta para agregar una nueva tarea
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    completed = False
    cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, ?)", (title, completed))
    connection.commit()
    return jsonify({'message': 'Tarea agregada exitosamente!'})

# Ruta para marcar una tarea como completada
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (True, task_id))
    connection.commit()
    return jsonify({'message': 'Tarea marcada como completada!'})

# Ruta para eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connection.commit()
    return jsonify({'message': 'Tarea eliminada exitosamente!'})

if __name__ == '__main__':
    app.run(debug=True)

