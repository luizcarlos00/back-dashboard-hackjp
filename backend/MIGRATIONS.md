# Database Migrations with Alembic 🗄️

Este projeto usa **Alembic** para gerenciar migrations do banco de dados com SQLAlchemy ORM.

## 📋 Setup Inicial

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

Crie arquivo `.env`:

```bash
# Option 1: DATABASE_URL completo
DATABASE_URL=postgresql://postgres:sua_senha@db.xxxxx.supabase.co:5432/postgres

# Option 2: Apenas senha (constrói URL automaticamente)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_DB_PASSWORD=sua_senha
```

### 3. Obter Credenciais do Supabase

1. Vá para seu projeto no Supabase
2. Settings → Database
3. Copy:
   - **Host**: `db.xxxxx.supabase.co`
   - **Database password**: sua senha do banco

## 🚀 Comandos Alembic

### Criar Nova Migration

```bash
# Auto-gerar migration baseada nos models
alembic revision --autogenerate -m "descrição da mudança"

# Ou criar migration vazia
alembic revision -m "descrição da mudança"
```

### Aplicar Migrations

```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Aplicar até uma revisão específica
alembic upgrade <revision_id>

# Aplicar próxima migration
alembic upgrade +1
```

### Reverter Migrations

```bash
# Reverter última migration
alembic downgrade -1

# Reverter todas as migrations
alembic downgrade base

# Reverter até uma revisão específica
alembic downgrade <revision_id>
```

### Ver Status

```bash
# Ver migration atual
alembic current

# Ver histórico
alembic history

# Ver migrations pendentes
alembic show <revision_id>
```

## 📝 Workflow de Desenvolvimento

### 1. Modificar Models

Edite seus models em `app/db_models.py`:

```python
# Adicionar nova coluna
class User(Base):
    __tablename__ = "users"
    # ... campos existentes ...
    nova_coluna = Column(String(100))  # Nova coluna
```

### 2. Gerar Migration Automática

```bash
alembic revision --autogenerate -m "add nova_coluna to users"
```

Isso criará um arquivo em `alembic/versions/` com o código da migration.

### 3. Revisar Migration Gerada

Abra o arquivo gerado e verifique se está correto:

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('nova_coluna', sa.String(length=100)))

def downgrade() -> None:
    op.drop_column('users', 'nova_coluna')
```

### 4. Aplicar Migration

```bash
alembic upgrade head
```

### 5. Verificar no Banco

Conecte no Supabase e verifique se a coluna foi criada.

## 🏗️ Setup Inicial do Banco (Primeira Vez)

Se for a primeira vez configurando o banco:

### Opção A: Usar SQL Schema Diretamente

```bash
# No Supabase SQL Editor, execute:
# app/database/schema.sql
```

Depois, crie a tabela de versões do Alembic:

```bash
alembic stamp head
```

### Opção B: Usar Alembic desde o início

```bash
# Criar migration inicial
alembic revision --autogenerate -m "initial migration"

# Aplicar
alembic upgrade head
```

## 🔧 Migrations Comuns

### Adicionar Coluna

```python
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255)))

def downgrade():
    op.drop_column('users', 'email')
```

### Remover Coluna

```python
def upgrade():
    op.drop_column('users', 'old_column')

def downgrade():
    op.add_column('users', sa.Column('old_column', sa.String(100)))
```

### Modificar Coluna

```python
def upgrade():
    op.alter_column('users', 'idade',
                    existing_type=sa.INTEGER(),
                    type_=sa.SmallInteger())

def downgrade():
    op.alter_column('users', 'idade',
                    existing_type=sa.SmallInteger(),
                    type_=sa.INTEGER())
```

### Criar Tabela

```python
def upgrade():
    op.create_table('new_table',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

def downgrade():
    op.drop_table('new_table')
```

### Adicionar Index

```python
def upgrade():
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', 'users')
```

## 🎯 Best Practices

1. **Sempre revise migrations auto-geradas** antes de aplicar
2. **Teste migrations localmente** antes de produção
3. **Faça backup** antes de migrations importantes
4. **Use migrations reversíveis** (implemente `downgrade()`)
5. **Commits pequenos**: uma migration por mudança lógica
6. **Nomes descritivos**: `add_email_to_users` não `update_db`

## ⚠️ Troubleshooting

### "Target database is not up to date"

```bash
# Ver versão atual
alembic current

# Sincronizar com estado atual
alembic stamp head
```

### "Can't locate revision identified by..."

```bash
# Limpar histórico e recomeçar
alembic stamp base
alembic upgrade head
```

### "Connection refused"

Verifique:
- DATABASE_URL está correto
- Senha do banco está correta
- Firewall do Supabase permite sua conexão
- Arquivo `.env` existe e está carregado

### Erro de import nos models

Certifique-se que `alembic/env.py` importa todos os models:

```python
from app.db_models import *
```

## 📚 Recursos

- **Alembic Docs**: https://alembic.sqlalchemy.org/
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org/
- **Supabase Database**: https://supabase.com/docs/guides/database

---

**Dica**: Durante desenvolvimento, você pode usar `alembic revision --autogenerate` frequentemente para gerar migrations automaticamente baseadas nos seus models.

