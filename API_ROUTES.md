# 📡 FeedBreak API - Guia Completo de Rotas

**Base URL:** `http://localhost:8000`

---

## 🏥 Health & Info

### GET `/health`
Verifica status da API
```bash
curl http://localhost:8000/health
```
**Response:**
```json
{
  "status": "ok",
  "message": "FeedBreak API is running",
  "version": "1.0.0"
}
```

### GET `/`
Informações da API
```bash
curl http://localhost:8000/
```

---

## 👤 Users (`/api/v1/users`)

### POST `/api/v1/users`
Criar ou atualizar usuário (upsert por device_id)

**Request Body:**
```json
{
  "device_id": "ABC123",
  "nome": "João Silva",
  "idade": 15,
  "interesses": ["matematica", "programacao"],
  "nivel_educacional": "medio"
}
```

**Response:**
```json
{
  "id": "uuid",
  "device_id": "ABC123",
  "nome": "João Silva",
  "idade": 15,
  "interesses": ["matematica", "programacao"],
  "nivel_educacional": "medio",
  "created_at": "2025-11-09T12:00:00",
  "last_active_at": "2025-11-09T12:00:00"
}
```

### GET `/api/v1/users/{device_id}`
Buscar usuário por device_id

**Example:**
```bash
curl http://localhost:8000/api/v1/users/ABC123
```

---

## 📚 Contents (`/api/v1/contents`)

### POST `/api/v1/contents`
Criar conteúdo com vídeos e atividades

**Request Body:**
```json
{
  "title": "Matemática - Frações",
  "description": "Aprenda frações de forma divertida",
  "publico_alvo": "fundamental",
  "category": "matematica",
  "is_active": true,
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
      "question": "Quanto é 1/2 + 1/4? Explique.",
      "order_index": 1
    }
  ]
}
```

### GET `/api/v1/contents`
Listar conteúdos

**Query Params:**
- `skip` (int): Paginação, padrão 0
- `limit` (int): Limite, padrão 100
- `publico_alvo` (string): Filtrar por público
- `category` (string): Filtrar por categoria
- `is_active` (bool): Filtrar por status

**Example:**
```bash
curl "http://localhost:8000/api/v1/contents?publico_alvo=fundamental&limit=10"
```

### GET `/api/v1/contents/{content_id}`
Buscar conteúdo específico (com vídeos e atividades)

**Example:**
```bash
curl http://localhost:8000/api/v1/contents/uuid-do-conteudo
```

### PUT `/api/v1/contents/{content_id}`
Atualizar conteúdo

**Request Body:**
```json
{
  "title": "Novo título",
  "publico_alvo": "medio",
  "is_active": false
}
```

### DELETE `/api/v1/contents/{content_id}`
Deletar conteúdo (e todos os vídeos/atividades)

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/v1/contents/uuid-do-conteudo
```

---

## 🎥 Videos (`/api/v1/videos`)

### POST `/api/v1/videos?content_id={id}`
Adicionar vídeo a um conteúdo

**Request Body:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "Título do vídeo",
  "quantity_until_e2e": 3,
  "order_index": 1
}
```

### GET `/api/v1/videos/{video_id}?include_url=true`
Buscar vídeo (com yt-dlp para URL real)

**Query Params:**
- `include_url` (bool): Se true, busca URL via yt-dlp (default: true)

**Example:**
```bash
curl "http://localhost:8000/api/v1/videos/uuid-do-video?include_url=true"
```

**Response:**
```json
{
  "id": "uuid",
  "content_id": "uuid",
  "video_id": "dQw4w9WgXcQ",
  "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "title": "Never Gonna Give You Up",
  "thumbnail_url": "https://...",
  "duration": 212,
  "quantity_until_e2e": 3,
  "order_index": 1,
  "created_at": "2025-11-09T12:00:00"
}
```

### GET `/api/v1/videos`
Listar vídeos

**Query Params:**
- `content_id` (string): Filtrar por conteúdo
- `include_url` (bool): Buscar URLs via yt-dlp (default: false para performance)
- `skip`, `limit`: Paginação

**Example:**
```bash
curl "http://localhost:8000/api/v1/videos?content_id=uuid&include_url=false"
```

### PUT `/api/v1/videos/{video_id}`
Atualizar vídeo

**Query Params:**
- `title` (string)
- `quantity_until_e2e` (int)
- `order_index` (int)

### DELETE `/api/v1/videos/{video_id}`
Deletar vídeo

---

## 📝 Activities (`/api/v1/activities`)

### POST `/api/v1/activities?content_id={id}`
Adicionar atividade E2E a um conteúdo

**Request Body:**
```json
{
  "question": "Explique o conceito de frações.",
  "order_index": 1
}
```

### GET `/api/v1/activities/{activity_id}`
Buscar atividade

### GET `/api/v1/activities`
Listar atividades

**Query Params:**
- `content_id` (string): Filtrar por conteúdo
- `skip`, `limit`: Paginação

### PUT `/api/v1/activities/{activity_id}`
Atualizar atividade

### DELETE `/api/v1/activities/{activity_id}`
Deletar atividade

---

## 💬 Activity Responses (`/api/v1/responses`)

### POST `/api/v1/responses`
Criar resposta (texto)

**Request Body:**
```json
{
  "device_id": "ABC123",
  "activity_id": "uuid-da-atividade",
  "answer": "Minha resposta em texto...",
  "grau_aprendizagem": 0.85,
  "responded": true
}
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "activity_id": "uuid",
  "answer": "Minha resposta...",
  "grau_aprendizagem": 0.85,
  "responded": true,
  "created_at": "2025-11-09T12:00:00"
}
```

### POST `/api/v1/responses/audio`
Criar resposta (áudio)

**Request (multipart/form-data):**
- `device_id`: string
- `activity_id`: string
- `audio`: file (mp3, wav, etc)

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/responses/audio \
  -F "device_id=ABC123" \
  -F "activity_id=uuid" \
  -F "audio=@resposta.mp3"
```

### GET `/api/v1/responses/{response_id}`
Buscar resposta

### GET `/api/v1/responses`
Listar respostas

**Query Params:**
- `user_device_id` (string): Filtrar por usuário
- `activity_id` (string): Filtrar por atividade
- `skip`, `limit`: Paginação

**Example:**
```bash
curl "http://localhost:8000/api/v1/responses?user_device_id=ABC123"
```

### PUT `/api/v1/responses/{response_id}`
Atualizar resposta (ex: adicionar grau_aprendizagem após IA avaliar)

**Request Body:**
```json
{
  "grau_aprendizagem": 0.75
}
```

### DELETE `/api/v1/responses/{response_id}`
Deletar resposta

---

## 📊 Progress (`/api/v1/progress`)

### POST `/api/v1/progress/watch`
Marcar vídeo como assistido

**Request Body:**
```json
{
  "device_id": "ABC123",
  "video_id": "uuid-do-video",
  "watched": true
}
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "video_id": "uuid",
  "watched": true,
  "watched_at": "2025-11-09T12:00:00"
}
```

### GET `/api/v1/progress/next-video` ⭐ IMPORTANTE
Buscar próximo vídeo e verificar se deve disparar E2E

**Query Params:**
- `device_id` (string): OBRIGATÓRIO
- `content_id` (string): Opcional

**Example:**
```bash
curl "http://localhost:8000/api/v1/progress/next-video?device_id=ABC123&content_id=uuid"
```

**Response:**
```json
{
  "video": {
    "id": "uuid",
    "video_id": "dQw4w9WgXcQ",
    "url": "https://youtube.com/watch?v=...",
    "title": "Vídeo X",
    "thumbnail_url": "https://...",
    "duration": 180,
    "quantity_until_e2e": 3
  },
  "watched_count": 2,
  "should_trigger_e2e": false,
  "next_activity": null
}
```

**Quando `should_trigger_e2e=true`:**
```json
{
  "video": null,
  "watched_count": 3,
  "should_trigger_e2e": true,
  "next_activity": {
    "id": "uuid",
    "question": "Pergunta da atividade..."
  }
}
```

### GET `/api/v1/progress/user/{device_id}`
Buscar todo progresso do usuário

**Query Params:**
- `content_id` (string): Filtrar por conteúdo

### GET `/api/v1/progress/stats/{device_id}`
Estatísticas do usuário

**Response:**
```json
{
  "user_id": "uuid",
  "device_id": "ABC123",
  "total_videos_watched": 12,
  "total_activities_completed": 5,
  "avg_learning_grade": 0.78,
  "contents_in_progress": 3
}
```

---

## 📈 Dashboard (`/api/v1/dashboard`)

### GET `/api/v1/dashboard/stats`
Estatísticas gerais

**Response:**
```json
{
  "total_users": 150,
  "total_videos": 45,
  "total_activities": 30,
  "total_video_watches": 1250,
  "total_activity_responses": 320,
  "avg_grau_aprendizagem": 0.78,
  "most_popular_content": "Matemática - Frações"
}
```

### GET `/api/v1/dashboard/users`
Estatísticas de usuários

**Query Params:**
- `skip`, `limit`: Paginação
- `order_by`: videos_watched | activities_completed | avg_grade

### GET `/api/v1/dashboard/content/{content_id}/stats`
Estatísticas de um conteúdo

### GET `/api/v1/dashboard/leaderboard`
Ranking dos melhores usuários

**Query Params:**
- `limit` (int): Número de usuários, padrão 10

---

## 🎨 Dashboard Frontend (`/api/v1/dashboard-frontend`)

### GET `/api/v1/dashboard-frontend/students`
Lista estudantes no formato do dashboard

**Response:**
```json
[
  {
    "id": 1,
    "nome": "Ana Silva",
    "idade": 12,
    "escolaridade": "Fundamental",
    "conteudos": [
      {
        "id": "video-uuid",
        "tipo": "video",
        "titulo": "Matemática - Parte 1",
        "dificuldade": "Fácil",
        "concluido": true,
        "dataInicio": "2025-09-17"
      }
    ]
  }
]
```

### GET `/api/v1/dashboard-frontend/stats`
Estatísticas para dashboard

### GET `/api/v1/dashboard-frontend/content-distribution`
Distribuição de tipos de conteúdo

### GET `/api/v1/dashboard-frontend/difficulty-distribution`
Distribuição de dificuldades

---

## 🎯 Fluxo de Integração Mobile/App

### 1️⃣ **Criar/Atualizar Usuário**
```http
POST /api/v1/users
{
  "device_id": "DEVICE_UNIQUE_ID",
  "nome": "Nome do Usuário",
  "idade": 15,
  "interesses": ["matematica"],
  "nivel_educacional": "medio"
}
```

### 2️⃣ **Buscar Próximo Vídeo**
```http
GET /api/v1/progress/next-video?device_id=DEVICE_UNIQUE_ID

Response:
{
  "video": {...},           // Dados do vídeo com URL
  "watched_count": 2,       // Quantos já assistiu
  "should_trigger_e2e": false,  // Se deve mostrar atividade
  "next_activity": null     // Atividade (se should_trigger_e2e=true)
}
```

### 3️⃣ **Marcar Vídeo como Assistido**
```http
POST /api/v1/progress/watch
{
  "device_id": "DEVICE_UNIQUE_ID",
  "video_id": "uuid-do-video",
  "watched": true
}
```

### 4️⃣ **Verificar se Deve Disparar E2E**
Após marcar como assistido, chamar novamente `/next-video`:
- Se `should_trigger_e2e=false`: Mostrar próximo vídeo
- Se `should_trigger_e2e=true`: Mostrar `next_activity`

### 5️⃣ **Responder Atividade (Texto)**
```http
POST /api/v1/responses
{
  "device_id": "DEVICE_UNIQUE_ID",
  "activity_id": "uuid-da-atividade",
  "answer": "Minha resposta em texto...",
  "grau_aprendizagem": 0.85,  // Pode ser calculado pela IA
  "responded": true
}
```

### 6️⃣ **Responder Atividade (Áudio)**
```http
POST /api/v1/responses/audio
Content-Type: multipart/form-data

device_id: DEVICE_UNIQUE_ID
activity_id: uuid-da-atividade
audio: [arquivo.mp3]
```

### 7️⃣ **Ver Estatísticas do Usuário**
```http
GET /api/v1/progress/stats/DEVICE_UNIQUE_ID

Response:
{
  "total_videos_watched": 12,
  "total_activities_completed": 5,
  "avg_learning_grade": 0.78,
  "contents_in_progress": 3
}
```

---

## 📱 Exemplo de Fluxo Completo (Mobile App)

```javascript
// 1. Login/Registro do usuário
const user = await fetch('http://api.com/api/v1/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    device_id: DeviceInfo.uniqueId,
    nome: "João Silva",
    idade: 15,
    interesses: ["matematica"],
    nivel_educacional: "medio"
  })
}).then(r => r.json());

// 2. Buscar próximo vídeo
const next = await fetch(
  `http://api.com/api/v1/progress/next-video?device_id=${DeviceInfo.uniqueId}`
).then(r => r.json());

if (next.should_trigger_e2e) {
  // Mostrar atividade E2E
  showActivity(next.next_activity);
} else {
  // Mostrar vídeo
  playVideo(next.video);
}

// 3. Após assistir vídeo
await fetch('http://api.com/api/v1/progress/watch', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    device_id: DeviceInfo.uniqueId,
    video_id: next.video.id,
    watched: true
  })
});

// 4. Verificar novamente
const nextCheck = await fetch(
  `http://api.com/api/v1/progress/next-video?device_id=${DeviceInfo.uniqueId}`
).then(r => r.json());

if (nextCheck.should_trigger_e2e) {
  // Agora mostrar atividade!
  showActivity(nextCheck.next_activity);
}

// 5. Quando responder atividade
await fetch('http://api.com/api/v1/responses', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    device_id: DeviceInfo.uniqueId,
    activity_id: nextCheck.next_activity.id,
    answer: "Minha resposta...",
    grau_aprendizagem: 0.85,  // Calcular com IA
    responded: true
  })
});

// 6. Ver estatísticas
const stats = await fetch(
  `http://api.com/api/v1/progress/stats/${DeviceInfo.uniqueId}`
).then(r => r.json());

console.log('Vídeos assistidos:', stats.total_videos_watched);
console.log('Média de aprendizagem:', stats.avg_learning_grade);
```

---

## 🔑 Headers Importantes

```http
Content-Type: application/json
Accept: application/json
```

Para upload de áudio:
```http
Content-Type: multipart/form-data
```

---

## ⚠️ Error Handling

**Status Codes:**
- `200` - Sucesso
- `201` - Criado com sucesso
- `204` - Deletado com sucesso
- `404` - Não encontrado
- `500` - Erro no servidor

**Error Response:**
```json
{
  "detail": "Mensagem de erro"
}
```

---

## 🧪 Testando

### Postman Collection

Importe esta URL base e teste todos os endpoints:
```
http://localhost:8000
```

### Swagger UI

Acesse a documentação interativa:
```
http://localhost:8000/docs
```

---

## 🎯 Endpoints Principais para App Mobile

| Endpoint | Método | Descrição | Uso no App |
|----------|--------|-----------|------------|
| `/api/v1/users` | POST | Criar/atualizar usuário | Login/Registro |
| `/api/v1/progress/next-video` | GET | Próximo vídeo + E2E check | **Mais importante!** |
| `/api/v1/progress/watch` | POST | Marcar assistido | Após vídeo |
| `/api/v1/responses` | POST | Responder (texto) | E2E texto |
| `/api/v1/responses/audio` | POST | Responder (áudio) | E2E áudio |
| `/api/v1/progress/stats/{device_id}` | GET | Estatísticas | Perfil |
| `/api/v1/contents` | GET | Listar conteúdos | Browse |

---

## 💡 Dicas de Integração

1. **Use sempre `device_id`** como identificador único do usuário
2. **Chame `/next-video`** após cada vídeo assistido para verificar E2E
3. **O campo `should_trigger_e2e`** indica quando mostrar atividade
4. **URLs dos vídeos** são geradas dinamicamente via yt-dlp
5. **`grau_aprendizagem`** pode ser calculado por IA ou manualmente (0.0-1.0)

---

**📚 Documentação Completa:** http://localhost:8000/docs

