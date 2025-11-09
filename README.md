# 🎓 FeedBreak - Plataforma de Micro-Learning

Plataforma educacional com vídeos curtos e avaliações End-to-End (E2E) personalizadas por IA.

## 🚀 Quick Start

### Pré-requisitos

- Docker e Docker Compose
- Chave da API OpenAI

### Configuração

1. **Clone o repositório**
```bash
git clone <repo-url>
cd back-dashboard-hackjp
```

2. **Configure a API Key da OpenAI**
```bash
cd backend
cp env.example .env
# Edite .env e adicione sua OPENAI_API_KEY
```

3. **Inicie os containers**
```bash
docker compose up -d
```

4. **Acesse a aplicação**
- Frontend Dashboard: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Popular com Dados de Teste

```bash
docker exec feedbreak-backend python seed_test_data.py
```

---

## 📋 Estrutura do Projeto

```
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── routers/      # Endpoints da API
│   │   ├── services/     # Serviços (YouTube, IA)
│   │   ├── db_models.py  # Modelos do banco
│   │   └── models.py     # Schemas Pydantic
│   ├── alembic/          # Migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/            # Frontend Next.js
│   ├── pages/
│   ├── components/
│   ├── types/
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## 🗄️ Banco de Dados

**SQLite** com 6 tabelas principais:

- **users** - Usuários do sistema
- **contents** - Conteúdos educacionais (centro da estrutura)
- **videos** - Vídeos do YouTube (armazena apenas ID)
- **activities** - Atividades E2E
- **user_video_progress** - Tracking de vídeos assistidos
- **user_activity_responses** - Respostas com grau de aprendizagem (0-1)

---

## 📡 API Endpoints

### Conteúdos
- `POST /api/v1/contents` - Criar conteúdo com vídeos e atividades
- `GET /api/v1/contents` - Listar conteúdos
- `GET /api/v1/contents/{id}` - Buscar conteúdo
- `PUT /api/v1/contents/{id}` - Atualizar conteúdo
- `DELETE /api/v1/contents/{id}` - Deletar conteúdo

### Vídeos
- `GET /api/v1/videos/{id}?include_url=true` - Buscar vídeo (com yt-dlp)
- `GET /api/v1/videos` - Listar vídeos

### Atividades
- `GET /api/v1/activities` - Listar atividades
- `GET /api/v1/activities/{id}` - Buscar atividade

### Progresso
- `POST /api/v1/progress/watch` - Marcar vídeo assistido
- `GET /api/v1/progress/next-video` - Próximo vídeo (com E2E check)
- `GET /api/v1/progress/stats/{device_id}` - Estatísticas do usuário

### Respostas
- `POST /api/v1/responses` - Responder atividade (texto)
- `POST /api/v1/responses/audio` - Responder atividade (áudio)
- `PUT /api/v1/responses/{id}` - Atualizar resposta (adicionar grau)

### Dashboard
- `GET /api/v1/dashboard/stats` - Estatísticas gerais
- `GET /api/v1/dashboard/users` - Estatísticas de usuários
- `GET /api/v1/dashboard-frontend/students` - Dados para o dashboard frontend

---

## 🎯 Fluxo do Sistema

1. Usuário assiste vídeos → `UserVideoProgress` (`watched=true`)
2. Sistema conta vídeos assistidos
3. A cada N vídeos (`quantity_until_e2e`):
   - `should_trigger_e2e=true`
   - Retorna próxima atividade
4. Usuário responde (texto ou áudio) → `UserActivityResponse`
5. IA avalia e adiciona `grau_aprendizagem` (0.0-1.0)
6. Dashboard mostra estatísticas

---

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **UV** - Gerenciador de pacotes Python (9x mais rápido)
- **yt-dlp** - Extração de vídeos do YouTube
- **OpenAI** - Avaliação de respostas por IA
- **LangChain** - Framework para IA

### Frontend
- **Next.js 16** - Framework React
- **TypeScript** - Type safety
- **Tailwind CSS** - Estilização
- **Recharts** - Gráficos

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **Alembic** - Migrations

---

## 🔧 Comandos Úteis

### Desenvolvimento

```bash
# Ver logs
docker compose logs -f backend
docker compose logs -f dashboard

# Reiniciar containers
docker compose restart

# Parar containers
docker compose down

# Rebuild
docker compose build --no-cache
docker compose up -d
```

### Banco de Dados

```bash
# Recriar banco
docker exec feedbreak-backend python init_new_db.py

# Popular com dados de teste
docker exec feedbreak-backend python seed_test_data.py

# Ver dados
docker exec feedbreak-backend python -c "
from app.database import SessionLocal
from app.db_models import User
db = SessionLocal()
for u in db.query(User).all():
    print(f'{u.nome} ({u.idade} anos)')
"
```

### Produção

```bash
# Build para produção
docker compose -f docker-compose.yml build

# Deploy
docker compose up -d
```

---

## 📊 Exemplo de Uso da API

### Criar Conteúdo

```bash
curl -X POST http://localhost:8000/api/v1/contents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Matemática - Frações",
    "publico_alvo": "fundamental",
    "category": "matematica",
    "videos": [
      {
        "video_id": "dQw4w9WgXcQ",
        "title": "Introdução às Frações",
        "quantity_until_e2e": 3,
        "order_index": 1
      }
    ],
    "activities": [
      {
        "question": "Quanto é 1/2 + 1/4? Explique seu raciocínio.",
        "order_index": 1
      }
    ]
  }'
```

### Buscar Próximo Vídeo

```bash
curl "http://localhost:8000/api/v1/progress/next-video?device_id=ABC123"
```

### Marcar Vídeo Assistido

```bash
curl -X POST http://localhost:8000/api/v1/progress/watch \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "ABC123",
    "video_id": "video-uuid",
    "watched": true
  }'
```

### Responder Atividade

```bash
curl -X POST http://localhost:8000/api/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "ABC123",
    "activity_id": "activity-uuid",
    "answer": "3/4, porque somamos os numeradores...",
    "grau_aprendizagem": 0.85
  }'
```

---

## 🔑 Variáveis de Ambiente

### Backend (`backend/.env`)

```env
OPENAI_API_KEY=sk-your-key-here
PORT=8000
DATABASE_URL=sqlite:///./db/feedbreak.db
```

### Frontend (via Docker Compose)

```yaml
NEXT_PUBLIC_API_URL=http://backend:8000
NODE_ENV=production
PORT=3000
```

---

## 🐳 Docker

### Arquitetura

- **backend** - Python 3.11 com UV package manager
- **dashboard** - Node 20 Alpine com Next.js standalone
- **Network** - Bridge network para comunicação entre containers
- **Volumes** - Named volume para persistência do banco

### Health Checks

Ambos os containers têm health checks configurados:
- Backend: `curl http://localhost:8000/health`
- Frontend: Verifica se a porta 3000 está respondendo

---

## 📝 Features Principais

### ✨ **Micro-Learning**
- Vídeos curtos educacionais
- Integração com YouTube (yt-dlp)
- Tracking de progresso por usuário

### 🎯 **Avaliações E2E Personalizadas**
- Atividades disparadas a cada N vídeos
- Respostas em texto ou áudio
- Avaliação por IA (grau de aprendizagem 0-1)

### 📊 **Dashboard Analítico**
- Estatísticas em tempo real
- Filtros avançados
- Gráficos interativos
- Ranking de estudantes

### 🎥 **Gestão de Conteúdo**
- CRUD completo de conteúdos
- Vídeos por público-alvo
- Atividades personalizáveis

---

## 🔒 Segurança

- CORS configurado (ajustar para produção)
- Validação de dados com Pydantic
- Sanitização de inputs
- Upload de arquivos protegido

---

## 📈 Performance

- **UV Package Manager**: 9x mais rápido que pip
- **Docker Build**: ~50% mais rápido
- **Next.js Standalone**: Build otimizado
- **yt-dlp**: URLs dinâmicas sempre atualizadas

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto foi desenvolvido para o Hackathon JP.

---

## 👥 Autores

Desenvolvido com ❤️ para o Hackathon JP

---

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker compose logs`
2. Confirme que os containers estão healthy: `docker ps`
3. Teste a API: `curl http://localhost:8000/health`
4. Verifique se há dados: `docker exec feedbreak-backend python seed_test_data.py`

---

**🚀 Ready to Production!**
