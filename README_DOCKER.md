# 🐳 Docker Setup - FeedBreak Backend

Guia completo para rodar o projeto usando Docker.

## 📋 Pré-requisitos

- Docker instalado ([Instalar Docker](https://docs.docker.com/get-docker/))
- Docker Compose instalado (geralmente vem com Docker Desktop)

## 🚀 Quick Start

### 1. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cd backend
cp .env.docker .env
```

Edite o arquivo `.env` e adicione sua chave OpenAI:
```bash
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 2. Iniciar o Projeto

Na raiz do projeto, execute:

```bash
# Build e iniciar containers
docker-compose up --build

# Ou em modo detached (background)
docker-compose up -d --build
```

### 3. Acessar a API

- **API Base:** http://localhost:8000
- **Documentação Swagger:** http://localhost:8000/docs
- **Documentação ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📦 Comandos Úteis

### Gerenciar Containers

```bash
# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Ver logs
docker-compose logs -f

# Ver logs apenas do backend
docker-compose logs -f backend

# Reiniciar serviço
docker-compose restart backend
```

### Executar Comandos no Container

```bash
# Acessar shell do container
docker-compose exec backend bash

# Executar script Python
docker-compose exec backend python init_db.py

# Ver processos
docker-compose ps

# Ver uso de recursos
docker stats
```

### Desenvolvimento

```bash
# Rebuild após mudanças no Dockerfile ou requirements.txt
docker-compose up --build

# Rebuild forçado (sem cache)
docker-compose build --no-cache

# Ver imagens
docker images

# Limpar imagens não utilizadas
docker image prune -a
```

## 🗄️ Gerenciamento do Banco de Dados

### Inicializar Banco de Dados

```bash
# Criar tabelas
docker-compose exec backend python init_db.py

# Popular com dados de exemplo (se seed_db.py estiver funcionando)
docker-compose exec backend python seed_db.py

# Recriar banco do zero
docker-compose exec backend python init_db.py --drop
```

### Backup do Banco

```bash
# Copiar banco de dados do container
docker cp feedbreak-backend:/app/feedbreak.db ./backup_$(date +%Y%m%d).db

# Restaurar backup
docker cp ./backup_20231109.db feedbreak-backend:/app/feedbreak.db
```

## 📁 Estrutura de Volumes

O Docker Compose monta os seguintes volumes:

- `./backend:/app` - Código fonte (hot reload)
- `./backend/feedbreak.db:/app/feedbreak.db` - Banco de dados
- `./backend/uploads:/app/uploads` - Arquivos de upload

Isso significa que:
- ✅ Mudanças no código são refletidas automaticamente
- ✅ Dados do banco persistem após reiniciar
- ✅ Uploads são mantidos

## 🔧 Troubleshooting

### Porta já em uso

Se a porta 8000 já estiver em uso, edite `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # Muda porta externa para 8001
```

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs backend

# Verificar health check
docker inspect feedbreak-backend | grep -A 10 Health
```

### Banco de dados corrompido

```bash
# Parar containers
docker-compose down

# Deletar banco
rm backend/feedbreak.db

# Reiniciar e recriar banco
docker-compose up -d
docker-compose exec backend python init_db.py
```

### Limpar tudo e começar do zero

```bash
# Parar e remover tudo
docker-compose down -v

# Remover imagens
docker-compose rm -f
docker rmi back-dashboard-hackjp-backend

# Rebuild completo
docker-compose up --build
```

## 🌐 Variáveis de Ambiente

Arquivo `.env` suporta:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Server
PORT=8000

# Database
DATABASE_URL=sqlite:///./feedbreak.db

# Logging
LOG_LEVEL=info  # debug, info, warning, error
```

## 🔐 Segurança

⚠️ **IMPORTANTE:**

1. ❌ NUNCA commite o arquivo `.env` com suas chaves
2. ✅ Use `.env.docker` como template
3. ✅ Adicione `.env` ao `.gitignore` (já feito)
4. ✅ Em produção, use secrets do Docker ou variáveis de ambiente do host

## 📊 Monitoramento

### Health Check

O container possui health check automático:

```bash
# Ver status
docker-compose ps

# Ver detalhes do health check
docker inspect feedbreak-backend --format='{{json .State.Health}}' | python -m json.tool
```

### Logs

```bash
# Logs em tempo real
docker-compose logs -f

# Últimas 100 linhas
docker-compose logs --tail=100

# Logs com timestamp
docker-compose logs -f --timestamps
```

## 🚢 Deploy em Produção

### Para produção, considere:

1. **Remover hot reload:**
   - No `Dockerfile`, remova `--reload` do CMD

2. **Use variáveis de ambiente do host:**
   ```bash
   docker run -e OPENAI_API_KEY=$OPENAI_API_KEY ...
   ```

3. **Configure HTTPS** (use nginx como proxy reverso)

4. **Use banco de dados externo** (PostgreSQL recomendado)

5. **Configure logs estruturados**

6. **Adicione monitoramento** (Prometheus, Grafana)

## 📚 Mais Informações

- [Documentação Docker](https://docs.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI com Docker](https://fastapi.tiangolo.com/deployment/docker/)

---

**Dúvidas?** Verifique os logs: `docker-compose logs -f`

