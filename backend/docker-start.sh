#!/bin/bash
echo "🐳 Iniciando FeedBreak Backend..."

mkdir -p /app/db

if [ ! -f "/app/db/feedbreak.db" ]; then
    echo "📊 Criando banco de dados..."
    python init_new_db.py
    echo "✅ Banco criado!"
else
    echo "✅ Banco encontrado!"
fi

mkdir -p uploads/audio

echo "🚀 Iniciando servidor..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

