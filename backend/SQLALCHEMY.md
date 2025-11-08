# FeedBreak Backend - SQLAlchemy ORM

## 🎯 Mudança para SQLAlchemy

O projeto agora usa **SQLAlchemy ORM** ao invés de queries diretas do Supabase para interagir com o banco de dados PostgreSQL.

### Vantagens:
- ✅ **Type safety** com models Python
- ✅ **Relationships** automáticos entre tabelas  
- ✅ **Migrations** com Alembic
- ✅ **Query builder** poderoso e intuitivo
- ✅ **Testabilidade** melhorada
- ✅ **Portabilidade** entre diferentes bancos SQL

## 📦 Estrutura

```
app/
├── database.py       # Configuração SQLAlchemy + session
├── db_models.py      # Models ORM (User, Video, etc)
├── models.py         # Pydantic models (request/response)
└── routers/          # Endpoints FastAPI
```

## 🔧 Configuração

### 1. Variáveis de Ambiente

Adicione no `.env`:

```bash
# Opção 1: DATABASE_URL completo
DATABASE_URL=postgresql://postgres:senha@db.xxxxx.supabase.co:5432/postgres

# Opção 2: Apenas senha (constrói URL automaticamente)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_DB_PASSWORD=sua_senha_aqui
```

### 2. Models Disponíveis

**app/db_models.py:**
- `User` - Perfis de usuários
- `Video` - Vídeos educativos
- `UserProgress` - Progresso de visualização
- `Question` - Perguntas E2E
- `Answer` - Respostas dos usuários
- `E2EPrompt` - Prompts base

## 💻 Como Usar nos Routers

### Exemplo Básico

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User

router = APIRouter()

@router.get("/users/{device_id}")
async def get_user(device_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.device_id == device_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": str(user.id), "nome": user.nome}
```

### CRUD Operations

#### Create
```python
new_user = User(
    device_id="android-123",
    nome="João",
    idade=25,
    nivel_educacional="superior"
)
db.add(new_user)
db.commit()
db.refresh(new_user)  # Atualiza com dados do banco
```

#### Read
```python
# Um registro
user = db.query(User).filter(User.device_id == "android-123").first()

# Múltiplos registros
users = db.query(User).filter(User.idade >= 18).all()

# Com limit e offset
users = db.query(User).limit(10).offset(20).all()

# Count
total = db.query(User).count()
```

#### Update
```python
user = db.query(User).filter(User.device_id == "android-123").first()
user.nome = "João Silva"
user.last_active_at = datetime.now()
db.commit()
```

#### Delete
```python
user = db.query(User).filter(User.device_id == "android-123").first()
db.delete(user)
db.commit()
```

### Joins e Relationships

```python
# Eager loading com join
from sqlalchemy.orm import joinedload

user = db.query(User) \
    .options(joinedload(User.progress)) \
    .filter(User.device_id == "android-123") \
    .first()

# Acessar vídeos assistidos
for progress in user.progress:
    print(progress.video.title)

# Join manual
results = db.query(Answer, User.nome, Video.title) \
    .join(User, Answer.user_id == User.id) \
    .join(Video, Answer.video_id == Video.id) \
    .all()
```

### Aggregations

```python
from sqlalchemy import func

# Count por categoria
stats = db.query(
    Video.category,
    func.count(Video.id).label('total')
).group_by(Video.category).all()

# Average
avg_score = db.query(func.avg(Answer.quality_score)).scalar()

# Sum
total_views = db.query(func.sum(Video.view_count)).scalar()
```

### Filtros Avançados

```python
from sqlalchemy import and_, or_, not_

# AND
users = db.query(User).filter(
    and_(
        User.idade >= 18,
        User.nivel_educacional == "superior"
    )
).all()

# OR
users = db.query(User).filter(
    or_(
        User.idade < 18,
        User.idade > 65
    )
).all()

# NOT IN
watched_ids = [uuid1, uuid2, uuid3]
unwatched = db.query(Video).filter(
    ~Video.id.in_(watched_ids)
).all()

# LIKE
users = db.query(User).filter(User.nome.like("%Silva%")).all()
```

## 🔄 Migrations com Alembic

### Criar Migration

```bash
# Auto-gerar baseado nos models
alembic revision --autogenerate -m "add email to users"

# Manual
alembic revision -m "custom migration"
```

### Aplicar Migrations

```bash
# Todas pendentes
alembic upgrade head

# Uma específica
alembic upgrade +1
```

### Reverter

```bash
alembic downgrade -1
```

## ⚠️ Importante

### Sempre use try/except com rollback

```python
try:
    # operações no banco
    db.commit()
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
```

### UUIDs como strings nas responses

```python
return {"id": str(user.id)}  # UUID para string
```

### Arrays vazios como default

```python
interesses = Column(ARRAY(Text), default=[])
# Retorna [] ao invés de None
```

## 📚 Documentação

- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Alembic**: https://alembic.sqlalchemy.org/
- **FastAPI + SQLAlchemy**: https://fastapi.tiangolo.com/tutorial/sql-databases/

## 🆚 Antes vs Depois

### Antes (Supabase Client)
```python
user = supabase.table("users") \
    .select("*") \
    .eq("device_id", device_id) \
    .execute()

if user.data:
    return user.data[0]
```

### Depois (SQLAlchemy ORM)
```python
user = db.query(User).filter(User.device_id == device_id).first()

if user:
    return user
```

---

**Nota**: Supabase Storage continua sendo usado para arquivos de áudio através de `supabase_storage` em `config.py`.
