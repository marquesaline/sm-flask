from flask import Flask, jsonify, request
from models import db, Tarefa
from tarefas import tarefas
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/tarefas')
def get_tarefas():
    status = request.args.get('status')
    if status:
        filtered_tarefas = []
        for tarefa in tarefas:
            if tarefa['status'] == status:
                filtered_tarefas.append(tarefa)

        return jsonify(filtered_tarefas)
    
    return jsonify(tarefas)

@app.route('/tarefa/<int:id>')
def get_tarefa(id):
    for tarefa in tarefas:
        if tarefa['id'] == id:
            return jsonify(tarefa)
    return jsonify({'error': 'Tarefa não encontrada'}), 404

@app.route('/tarefa', methods=['POST'])
def add_tarefa():
    nova_tarefa = request.json

    if not nova_tarefa or 'titulo' not in nova_tarefa:
        return jsonify({'error': 'Dados inválidos'}), 400
    
    new_tarefa = {
        'titulo': nova_tarefa['titulo'],
        'descricao': nova_tarefa.get('descricao', ''),
        'status': nova_tarefa.get('status', 'pendente')
    }
    new_tarefa['id'] = len(tarefas) + 1

    tarefas.append(new_tarefa)

    return jsonify(new_tarefa), 201

@app.route('/tarefa/<int:id>', methods=['PUT'])
def update_tarefa(id):
    updated_data = request.json
    if not updated_data:
        return jsonify({'error': 'Dados inválidos'}), 400
    
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefa['titulo'] = updated_data.get('titulo', tarefa['titulo'])
            tarefa['descricao'] = updated_data.get('descricao', tarefa['descricao'])
            tarefa['status'] = updated_data.get('status', tarefa['status'])
            return jsonify(tarefa), 200
    
    return jsonify({'error': 'Tarefa não encontrada'}), 404


@app.route('/tarefa/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    for tarefa in tarefas:
        if tarefa['id'] == id:
            tarefas.remove(tarefa)
            return jsonify({'message': 'Tarefa deletada com sucesso'}), 200

    return jsonify({'error': 'Tarefa não encontrada'}), 404


with app.app_context():
    db.create_all()