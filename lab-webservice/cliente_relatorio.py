import requests

id_prod = input("Digite o ID do produto: ")

url_flask = f"http://localhost:5000/detalhes/{id_prod}"
url_node = f"http://localhost:3000/estoque/{id_prod}"

try:
    resp_flask = requests.get(url_flask)
    resp_node = requests.get(url_node)

    if resp_flask.status_code == 200 and resp_node.status_code == 200:
        dados_fiscais = resp_flask.json()
        dados_estoque = resp_node.json()
        
        print(f"ID: {id_prod} | Nome: {dados_estoque['nome']} | Preço: R$ {dados_fiscais['preco']} | Estoque: {dados_estoque['estoque']}")
    else:
        # Se for erro 400, o JSON padronizado do Exercício 5 será capturado aqui
        print(f"Erro Node: {resp_node.json()}")
        print(f"Erro Flask: {resp_flask.json()}")
except Exception as e:
    print(f"Erro de conexão: {e}")