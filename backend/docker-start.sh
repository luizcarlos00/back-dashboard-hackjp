#!/bin/bash
# Script de inicialização do container Docker

echo "🐳 Iniciando FeedBreak Backend..."

# Verificar se o banco existe, se não, criar
if [ ! -f "/app/feedbreak.db" ]; then
    echo "📊 Banco de dados não encontrado. Criando..."
    python init_db.py
    echo "✅ Banco de dados criado!"
fi

# Criar diretórios necessários
mkdir -p uploads/audio

echo "🚀 Iniciando servidor..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

