import requests

urls = ["http://localhost:5000/status", "http://localhost:3000/status"]

def checar_status(lista_urls):
    for url in lista_urls:
        try:
            resposta = requests.get(url).json()
            print(f"Serviço: {resposta['service']} | Status: {resposta['status']} | Hora: {resposta['timestamp']}")
        except:
            print(f"Erro ao conectar na URL: {url}")

checar_status(urls)