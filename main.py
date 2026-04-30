import json
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Criação do app Flask e definição da pasta estática como a atual (.)
app = Flask(__name__, static_folder='.')
CORS(app) # Permite requisições do frontend

DATA_FILE = 'dados.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    # Retorna o arquivo index.html da pasta atual
    return send_from_directory('.', 'index.html')

@app.route('/api/processos', methods=['GET'])
def get_processos():
    data = load_data()
    return jsonify(data)

@app.route('/api/processos', methods=['POST'])
def add_processo():
    data = load_data()
    new_processo = request.json
    
    # Gerar um novo ID sequencial
    new_id = 1
    if data:
        new_id = max(item.get('id', 0) for item in data) + 1
        
    new_processo['id'] = new_id
    data.append(new_processo)
    save_data(data)
    
    return jsonify(new_processo), 201

@app.route('/api/processos/<int:processo_id>', methods=['PUT'])
def update_processo(processo_id):
    data = load_data()
    updated_data = request.json
    
    for item in data:
        if item.get('id') == processo_id:
            # Atualiza os campos necessários
            if 'status' in updated_data:
                item['status'] = updated_data['status']
            if 'pendencias' in updated_data:
                item['pendencias'] = updated_data['pendencias']
                
            save_data(data)
            return jsonify(item)
            
    return jsonify({'error': 'Processo não encontrado'}), 404

if __name__ == '__main__':
    print("="*50)
    print("SISTEMA DE GESTÃO DE PROCESSOS RK")
    print("Acesse no navegador: http://127.0.0.1:5000")
    print("="*50)
    app.run(debug=True, port=5000)
