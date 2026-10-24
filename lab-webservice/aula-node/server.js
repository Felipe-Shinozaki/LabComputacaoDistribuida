const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

// Base de dados (Exercício Preparação)
const produtos_estoque = {
    "1": {"nome": "Dell XPS 13", "estoque": 10}, 
    "2": {"nome": "Monitor LG 29", "estoque": 5}
};
const produtos_comerciais = {}; // Para o Exercicio 4

// Validador (Exercício 5)
function validarId(req, res, next) {
    const id = Number(req.params.id);
    if (!Number.isInteger(id) || id < 0) {
        return res.status(400).json({"error": "INVALID_ID", "message": " ID deve ser um inteiro positivo"});
    }
    next();
}

// Rota base para o Estoque (Exercício 1)
app.get('/estoque/:id', validarId, (req, res) => {
    const produto = produtos_estoque[req.params.id];
    if (produto) res.json(produto);
    else res.status(404).json({error: "NOT_FOUND", message: "Produto não encontrado"});
});

// Rota Proxy Server-to-Server (Exercício 2)
app.get('/api/full-info/:id', validarId, async (req, res) => {
    try {
        const id = req.params.id;
        const estoque = produtos_estoque[id];
        
        // Fetch para o servidor Flask
        const responseFlask = await fetch(`http://localhost:5000/detalhes/${id}`);
        const fiscal = await responseFlask.json();

        if (estoque && responseFlask.ok) {
            res.json({nome: estoque.nome, preco: fiscal.preco, estoque: estoque.estoque, categoria: fiscal.categoria});
        } else {
            res.status(404).json({error: "NOT_FOUND"});
        }
    } catch (error) {
        res.status(500).json({error: "Erro ao contatar o Flask"});
    }
});

// Rota de Status (Exercício 3)
app.get('/status', (req, res) => {
    res.json({
        "service": "Node.js",
        "status": "online",
        "timestamp": new Date().toISOString()
    });
});

// Rota de Cadastro distribuído (Exercício 4)
app.post('/cadastrar', async (req, res) => {
    const { id, nome, estoque, preco_base, categoria } = req.body;
    const nomeCaixaAlta = nome.toUpperCase();

    const payloadFlask = { id, preco_base, categoria };

    try {
        const response = await fetch('http://localhost:5000/fiscal/cadastrar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payloadFlask)
        });

        if (response.status === 201) {
            produtos_comerciais[id] = { nome: nomeCaixaAlta, estoque: estoque };
            res.status(201).json({mensagem: "Cadastro completo distribuído com sucesso!", produto: produtos_comerciais[id]});
        } else {
            res.status(500).json({erro: "Falha ao sincronizar com servidor fiscal."});
        }
    } catch (error) {
        res.status(500).json({erro: "Erro de comunicação interna."});
    }
});

app.listen(PORT, () => {
    console.log(`Servidor Node rodando na porta ${PORT}`);
});