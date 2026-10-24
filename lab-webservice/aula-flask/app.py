from flask import Flask, jsonify, request
from datetime import datetime, timezone

app = Flask(__name__)

# Base de dados (Exercício Preparação)
produtos_fiscais = {
    "1": {"preco": 2500.0, "categoria": "Laptops"}, 
    "2": {"preco": 1200.0, "categoria": "Monitores"}
}
produtos_tecnicos = {} # Para o Exercicio 4

# Função validadora (Exercício 5)
def validar_id(id_str):
    try:
        val = int(id_str)
        if val < 0:
            return False
        return True
    except ValueError:
        return False

# Rota para o Exercício 1 e 2
@app.route('/detalhes/<id>', methods=['GET'])
def get_detalhes(id):
    if not validar_id(id):
        return jsonify({"error": "INVALID_ID", "message": " ID deve ser um inteiro positivo"}), 400
    
    produto = produtos_fiscais.get(id)
    if produto:
        return jsonify(produto)
    return jsonify({"error": "NOT_FOUND", "message": "Produto não encontrado"}), 404

# Rota de Status (Exercício 3)
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "service": "Flask",
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

# Rota de Cadastro (Exercício 4)
@app.route('/fiscal/cadastrar', methods=['POST'])
def cadastrar_fiscal():
    dados = request.json
    preco_calculado = float(dados['preco_base']) * 1.20 # +20% imposto
    produtos_tecnicos[str(dados['id'])] = {
        "preco": preco_calculado,
        "categoria": dados['categoria']
    }
    return jsonify({"mensagem": "Cadastrado com sucesso no Flask"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)