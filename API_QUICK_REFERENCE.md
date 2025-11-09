# 📱 API Quick Reference - FeedBreak

**Base URL:** `http://localhost:8000` ou `https://seu-dominio.com`

---

## 🚀 Rotas Principais para App Mobile

| Método | Endpoint | Descrição | Params/Body |
|--------|----------|-----------|-------------|
| **POST** | `/api/v1/users` | Criar/atualizar usuário | `{device_id, nome, idade, interesses[], nivel_educacional}` |
| **GET** | `/api/v1/users/{device_id}` | Buscar usuário | - |
| **GET** | `/api/v1/progress/next-video` ⭐ | Próximo vídeo + E2E check | `?device_id=XXX` |
| **POST** | `/api/v1/progress/watch` | Marcar vídeo assistido | `{device_id, video_id, watched}` |
| **POST** | `/api/v1/responses` | Responder atividade (texto) | `{device_id, activity_id, answer, grau_aprendizagem}` |
| **POST** | `/api/v1/responses/audio` | Responder atividade (áudio) | FormData: `device_id, activity_id, audio` |
| **GET** | `/api/v1/progress/stats/{device_id}` | Estatísticas do usuário | - |

---

## 📋 Todas as Rotas

### Users (`/api/v1/users`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/` | Criar/atualizar usuário (upsert) |
| GET | `/{device_id}` | Buscar usuário |

### Contents (`/api/v1/contents`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/` | Criar conteúdo com vídeos e atividades |
| GET | `/` | Listar conteúdos (com filtros) |
| GET | `/{content_id}` | Buscar conteúdo específico |
| PUT | `/{content_id}` | Atualizar conteúdo |
| DELETE | `/{content_id}` | Deletar conteúdo |

### Videos (`/api/v1/videos`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/?content_id={id}` | Adicionar vídeo ao conteúdo |
| GET | `/{video_id}?include_url=true` | Buscar vídeo (com yt-dlp) |
| GET | `/` | Listar vídeos |
| PUT | `/{video_id}` | Atualizar vídeo |
| DELETE | `/{video_id}` | Deletar vídeo |

### Activities (`/api/v1/activities`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/?content_id={id}` | Adicionar atividade ao conteúdo |
| GET | `/{activity_id}` | Buscar atividade |
| GET | `/` | Listar atividades |
| PUT | `/{activity_id}` | Atualizar atividade |
| DELETE | `/{activity_id}` | Deletar atividade |

### Responses (`/api/v1/responses`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/` | Criar resposta (texto) |
| POST | `/audio` | Criar resposta (áudio) |
| GET | `/{response_id}` | Buscar resposta |
| GET | `/` | Listar respostas |
| PUT | `/{response_id}` | Atualizar resposta |
| DELETE | `/{response_id}` | Deletar resposta |

### Progress (`/api/v1/progress`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/watch` | Marcar vídeo assistido |
| GET | `/next-video` | **Próximo vídeo + E2E check** ⭐ |
| GET | `/user/{device_id}` | Progresso do usuário |
| GET | `/stats/{device_id}` | Estatísticas do usuário |

### Dashboard (`/api/v1/dashboard`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/stats` | Estatísticas gerais |
| GET | `/users` | Estatísticas de usuários |
| GET | `/content/{id}/stats` | Estatísticas de conteúdo |
| GET | `/leaderboard` | Ranking de usuários |

### Dashboard Frontend (`/api/v1/dashboard-frontend`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/students` | Lista estudantes (formato frontend) |
| GET | `/stats` | Estatísticas (formato frontend) |
| GET | `/content-distribution` | Distribuição de tipos |
| GET | `/difficulty-distribution` | Distribuição de dificuldade |

---

## 🎯 Fluxo Simplificado

```
1. POST /api/v1/users
   └─> Criar usuário com device_id

2. GET /api/v1/progress/next-video?device_id=XXX
   └─> Retorna vídeo OU atividade

3. Se retornou vídeo:
   └─> Usuário assiste
   └─> POST /api/v1/progress/watch
   └─> Voltar ao passo 2

4. Se should_trigger_e2e=true:
   └─> Mostrar atividade
   └─> POST /api/v1/responses (texto ou /audio)
   └─> Voltar ao passo 2
```

---

## 📊 Response Examples

### Next Video (normal)
```json
{
  "video": {
    "id": "uuid",
    "video_id": "dQw4w9WgXcQ",
    "url": "https://youtube.com/watch?v=...",
    "title": "Matemática - Parte 1",
    "duration": 180
  },
  "watched_count": 2,
  "should_trigger_e2e": false,
  "next_activity": null
}
```

### Next Video (E2E triggered)
```json
{
  "video": null,
  "watched_count": 3,
  "should_trigger_e2e": true,
  "next_activity": {
    "id": "uuid",
    "question": "Quanto é 1/2 + 1/4?"
  }
}
```

---

**📚 Documentação Detalhada:** `API_ROUTES.md`  
**🌐 Swagger UI:** http://localhost:8000/docs

