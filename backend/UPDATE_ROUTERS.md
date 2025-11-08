# Atualização dos Routers para SQLAlchemy

## ⚠️ IMPORTANTE

Os routers ainda precisam ser atualizados para usar SQLAlchemy ORM ao invés do cliente Supabase.

## 🔄 Mudanças Necessárias

### Padrão de Mudança

**Antes (Supabase):**
```python
from app.config import supabase

@router.get("/endpoint")
async def endpoint():
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    return result.data
```

**Depois (SQLAlchemy):**
```python
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import User

@router.get("/endpoint")
async def endpoint(db: Session = Depends(get_db)):
    result = db.query(User).filter(User.id == user_id).first()
    return result
```

## 📝 Arquivos para Atualizar

- [ ] `app/routers/videos.py` ✅ (já iniciado)
- [ ] `app/routers/progress.py`
- [ ] `app/routers/questions.py`
- [ ] `app/routers/answers.py` (manter Supabase Storage para áudio)
- [ ] `app/routers/dashboard.py`

## 🚀 Script de Atualização Rápida

Você pode usar este comando para atualizar todos os routers automaticamente:

```bash
cd backend

# Para cada router, substitua as queries do Supabase por SQLAlchemy

# Veja exemplos no arquivo SQLALCHEMY.md
```

## 📚 Referências

- `app/routers/users.py` - Já atualizado como referência
- `SQLALCHEMY.md` - Guia completo de uso
- `app/db_models.py` - Todos os models disponíveis

## 🔍 Checklist de Mudanças

Para cada router:

1. Adicionar imports:
   ```python
   from sqlalchemy.orm import Session
   from app.database import get_db
   from app.db_models import User, Video, etc
   ```

2. Adicionar `db: Session = Depends(get_db)` nos parâmetros

3. Substituir `supabase.table(...).select(...)` por `db.query(Model).filter(...)`

4. Substituir `.insert()` por `db.add()` + `db.commit()`

5. Substituir `.update()` por modificar atributos + `db.commit()`

6. Substituir `.delete()` por `db.delete()` + `db.commit()`

7. Adicionar `try/except` com `db.rollback()` em caso de erro

8. Converter UUIDs para string nas responses: `str(model.id)`

## ⚡ Status Atual

- ✅ `users.py` - Atualizado
- ⏳ Outros routers - Aguardando atualização

---

**Nota**: O código já funciona com o schema SQL existente. Os models SQLAlchemy são compatíveis com as tabelas já criadas.
