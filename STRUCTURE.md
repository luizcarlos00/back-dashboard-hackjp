# 📚 Estrutura do Projeto - Back Dashboard HackJP

## 📁 Visão Geral do Repositório

Este é um projeto fullstack com backend em **FastAPI** e frontend em **Next.js**, desenvolvido para o hackathon HackJP.

```
back-dashboard-hackjp/
├── backend/              # API FastAPI
├── dashboard/            # Frontend Next.js
├── docker-compose.yml    # Orquestração de containers
└── README.md            # Documentação principal
```

---

## 🔧 Backend (FastAPI)

### Estrutura de Diretórios

```
backend/
├── app/
│   ├── main.py              # Ponto de entrada da aplicação FastAPI
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── db_models.py         # Modelos SQLAlchemy (tabelas do banco)
│   ├── models.py            # Modelos Pydantic (validação de dados)
│   │
│   ├── database/            # Configuração de conexão com banco
│   │   └── __init__.py
│   │
│   ├── routers/             # Endpoints da API (organizados por recurso)
│   │   ├── users.py         # CRUD de usuários
│   │   ├── contents.py      # Gerenciamento de conteúdos
│   │   ├── videos.py        # Listagem e entrega de vídeos
│   │   ├── progress.py      # Tracking de progresso do usuário
│   │   ├── questions.py     # Geração de perguntas E2E
│   │   ├── answers.py       # Submissão e análise de respostas
│   │   └── dashboard.py     # Estatísticas e analytics
│   │
│   ├── services/            # Lógica de negócio e integrações
│   │   ├── langchain_analyzer.py  # Análise de respostas com IA
│   │   └── agent.py         # (se existir) Agente de criação de perguntas
│   │
│   └── data_rag/            # Dados para RAG (Retrieval Augmented Generation)
│       └── bncc.txt         # Base Nacional Comum Curricular
│
├── alembic/                 # Migrações de banco de dados
│   ├── env.py
│   ├── script.py.mako
│   └── versions/            # Arquivos de migração (criados pelo Alembic)
│       └── .gitkeep         # Mantém pasta no Git
│
├── uploads/                 # Arquivos enviados pelos usuários
│   └── audio/               # Áudios de respostas
│       └── .gitkeep         # Mantém pasta no Git
│
├── requirements.txt         # Dependências Python
├── Dockerfile               # Imagem Docker do backend
├── docker-start.sh          # Script de inicialização do container
├── alembic.ini              # Configuração do Alembic
├── env.example              # Template de variáveis de ambiente
├── env.docker.example       # Template para Docker
├── init_db.py               # Script para inicializar banco
├── seed_db.py               # Script para popular banco com dados de teste
├── test_api.py              # Testes da API
└── README.md                # Documentação detalhada do backend
```

### 🔑 Arquivos Principais

#### `app/main.py`
- **O que faz:** Ponto de entrada da aplicação FastAPI
- **Responsabilidades:**
  - Cria a instância do FastAPI
  - Configura CORS (Cross-Origin Resource Sharing)
  - Registra todos os routers (endpoints)
  - Configura logging
  - Define health checks

#### `app/config.py`
- **O que faz:** Gerencia configurações e variáveis de ambiente
- **Contém:** 
  - Chaves de API (OpenAI)
  - Configurações de banco de dados
  - Caminhos de uploads
  - Configurações de servidor

#### `app/db_models.py`
- **O que faz:** Define a estrutura das tabelas do banco de dados
- **Usa:** SQLAlchemy ORM
- **Tabelas principais:**
  - `users` - Perfis de usuários
  - `contents` - Conteúdos educacionais
  - `videos` - Vídeos educativos
  - `questions` - Perguntas E2E
  - `answers` - Respostas dos usuários
  - `progress` - Progresso de visualização

#### `app/models.py`
- **O que faz:** Define schemas de validação de dados
- **Usa:** Pydantic
- **Para que serve:** Valida dados de entrada/saída da API
- **Exemplo:** Garante que um usuário tenha nome, email válido, idade, etc.

### 📡 Routers (Endpoints)

Cada router é responsável por um conjunto de endpoints relacionados:

#### `routers/users.py`
```
POST   /api/v1/user            - Criar/atualizar usuário
GET    /api/v1/user/{id}       - Buscar usuário
```

#### `routers/videos.py`
```
GET    /api/v1/videos          - Listar vídeos
GET    /api/v1/videos/next     - Próximo vídeo personalizado
GET    /api/v1/videos/{id}     - Detalhes de um vídeo
```

#### `routers/progress.py`
```
POST   /api/v1/progress        - Registrar progresso
```

#### `routers/questions.py`
```
GET    /api/v1/questions       - Gerar pergunta E2E
```

#### `routers/answers.py`
```
POST   /api/v1/answer          - Enviar resposta (texto)
POST   /api/v1/answer/audio    - Enviar resposta (áudio)
```

#### `routers/dashboard.py`
```
GET    /api/v1/dashboard/stats - Estatísticas gerais
GET    /api/v1/dashboard/e2e   - Respostas para revisão
```

### 🤖 Services

#### `services/langchain_analyzer.py`
- **O que faz:** Analisa respostas dos usuários usando IA (GPT-4o-mini)
- **Funcionalidades:**
  - Avalia qualidade da resposta
  - Calcula score (0.0 - 1.0)
  - Identifica conceitos mencionados
  - Gera feedback construtivo
  - Determina aprovação (≥ 0.6)

#### `services/agent.py` (se existir)
- **O que faz:** Cria perguntas personalizadas usando RAG
- **Usa:** BNCC (Base Nacional Comum Curricular) como contexto

---

## 🎨 Dashboard (Next.js)

### Estrutura de Diretórios

```
dashboard/
├── components/              # Componentes React reutilizáveis
│   ├── charts/              # Gráficos e visualizações
│   │   ├── ContentTypeChart.tsx
│   │   ├── DifficultyDistribution.tsx
│   │   └── ProgressOverview.tsx
│   ├── DashboardStats.tsx   # Cards de estatísticas
│   ├── Filters.tsx          # Filtros de dados
│   ├── Header.tsx           # Cabeçalho
│   ├── Layout.tsx           # Layout base
│   ├── StudentCard.tsx      # Card de estudante
│   ├── StudentDetailModal.tsx # Modal de detalhes
│   └── ThemeProvider.tsx    # Provider de tema
│
├── pages/                   # Páginas Next.js (rotas automáticas)
│   ├── _app.tsx            # Wrapper da aplicação
│   └── index.tsx           # Página principal (dashboard)
│
├── types/                   # Definições TypeScript
│   └── index.ts
│
├── utils/                   # Funções utilitárias
│   └── mockData.ts         # Dados de exemplo
│
├── styles/                  # Estilos globais
│   └── globals.css
│
├── public/                  # Arquivos estáticos
│   └── students.json       # Dados mockados
│
├── package.json            # Dependências Node.js
├── tsconfig.json           # Configuração TypeScript
├── tailwind.config.js      # Configuração Tailwind CSS
└── README.md               # Documentação do frontend
```

---

## 🐳 Docker

### `docker-compose.yml`
- **O que faz:** Orquestra múltiplos containers
- **Services:**
  - `backend` - API FastAPI
  - `dashboard` - Frontend Next.js (se configurado)

### `backend/Dockerfile`
- **O que faz:** Define como construir a imagem do backend
- **Etapas:**
  1. Instala Python e dependências
  2. Copia código da aplicação
  3. Expõe porta 8000
  4. Roda a aplicação com uvicorn

---

## 🔐 Arquivos de Configuração

### `.gitignore`
**O que ignora:**
- `__pycache__/` e `*.pyc` - Cache Python
- `*.db`, `*.sqlite` - Bancos de dados locais
- `.env` - Variáveis de ambiente (NUNCA commitar!)
- `node_modules/` - Dependências Node.js
- `uploads/audio/*` - Arquivos de usuários
- `.git-rewrite/` - Arquivos temporários do Git

### `backend/.env` (NÃO commitado)
**Contém:**
```bash
OPENAI_API_KEY=sk-...        # Chave da API OpenAI
DATABASE_URL=sqlite:///...   # URL do banco de dados
PORT=8000                     # Porta do servidor
```

### `backend/env.example` (commitado)
**Template para criar `.env`** - mostra quais variáveis são necessárias sem expor valores reais

---

## 🗃️ Banco de Dados

### SQLite Local (`feedbreak.db`)
- **Tipo:** Banco relacional leve
- **Por que não commitar:**
  - Cresce com o tempo
  - Dados são específicos do ambiente local
  - Pode conter dados sensíveis
  - Causa conflitos de merge
- **Como gerenciar:**
  - Cada desenvolvedor cria seu próprio banco local
  - Use `init_db.py` ou `seed_db.py` para popular
  - Use migrações Alembic para sincronizar schema

### Alembic (Migrações)
- **O que faz:** Gerencia mudanças no schema do banco
- **Como funciona:**
  1. Você modifica `db_models.py`
  2. Roda `alembic revision --autogenerate`
  3. Alembic cria um arquivo de migração
  4. Roda `alembic upgrade head` para aplicar

---

## 🚀 Como Funciona o Fluxo Principal

### 1️⃣ Usuário acessa o app
```
Mobile App → POST /api/v1/user
           ← Perfil criado/atualizado
```

### 2️⃣ Solicita próximo vídeo
```
Mobile App → GET /api/v1/videos/next?device_id=X
           ← Vídeo personalizado baseado em interesses
```

### 3️⃣ Assiste e marca como completo
```
Mobile App → POST /api/v1/progress
           ← Progresso registrado
```

### 4️⃣ Após N vídeos, recebe pergunta E2E
```
Mobile App → GET /api/v1/questions?device_id=X&video_id=Y
           ← Pergunta personalizada
```

### 5️⃣ Responde (texto ou áudio)
```
Mobile App → POST /api/v1/answer
           ← IA analisa e retorna feedback + score
```

### 6️⃣ Dashboard visualiza dados
```
Dashboard → GET /api/v1/dashboard/stats
          ← Estatísticas agregadas
```

---

## 📦 Dependências Principais

### Backend (Python)
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **LangChain** - Framework para IA
- **OpenAI** - API de IA (GPT-4o-mini)
- **Uvicorn** - Servidor ASGI
- **Alembic** - Migrações de banco
- **yt-dlp** - Download de vídeos do YouTube

### Frontend (Node.js)
- **Next.js** - Framework React
- **React** - Biblioteca UI
- **TypeScript** - JavaScript tipado
- **Tailwind CSS** - Framework CSS utilitário

---

## 🛠️ Scripts Úteis

### Backend
```bash
# Instalar dependências
pip install -r requirements.txt

# Inicializar banco
python init_db.py

# Popular com dados de teste
python seed_db.py

# Rodar servidor (desenvolvimento)
python app/main.py

# Criar migração
alembic revision --autogenerate -m "Descrição"

# Aplicar migrações
alembic upgrade head
```

### Docker
```bash
# Subir tudo
docker-compose up --build

# Somente backend
docker-compose up backend

# Parar tudo
docker-compose down
```

---

## ⚠️ Boas Práticas

### ✅ FAÇA:
- Commite código, configurações, documentação
- Use `.env.example` como template
- Crie migrações para mudanças no banco
- Use `.gitkeep` para pastas vazias necessárias
- Documente funções e endpoints complexos

### ❌ NÃO FAÇA:
- Commite `.env` (contém senhas!)
- Commite `*.db` (banco de dados)
- Commite `__pycache__/` (cache Python)
- Commite `node_modules/` (dependências Node)
- Commite arquivos de usuários (`uploads/`)
- Commite chaves de API ou senhas

---

## 🔍 Como Investigar Problemas

### Backend não inicia?
1. Verifique `.env` existe e tem `OPENAI_API_KEY`
2. Rode `pip install -r requirements.txt`
3. Verifique logs no terminal

### Erros de banco?
1. Delete `feedbreak.db`
2. Rode `python init_db.py`
3. Rode `alembic upgrade head`

### CORS errors?
- Verifique configuração em `app/main.py`
- Para produção, defina origins específicas

---

## 📞 Recursos Adicionais

- **API Docs:** http://localhost:8000/docs (Swagger)
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

**Criado para Hackathon HackJP** 🚀

