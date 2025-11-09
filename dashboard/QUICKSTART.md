# 🚀 Quick Start Guide

## Dashboard Estudantil - TypeScript + Tailwind CSS

### Início Rápido (5 minutos)

```bash
# 1. Navegue até o diretório
cd dashboard

# 2. Instale as dependências (se ainda não instalou)
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

Abra [http://localhost:3000](http://localhost:3000) no navegador!

### 🎨 Recursos Principais

#### Dark Mode
- Clique no ícone 🌙/☀️ no canto superior direito
- Alterna automaticamente entre modo claro e escuro
- Salva sua preferência no localStorage

#### Filtros
Use a seção de filtros para:
- **Buscar** por nome do estudante
- **Filtrar** por faixa etária (10-30 anos)
- **Filtrar** por escolaridade (Fundamental, Médio, Superior)
- **Filtrar** por tipo de conteúdo (Vídeos, Atividades, Exercícios)
- **Filtrar** por dificuldade (Fácil, Médio, Difícil)
- Clique em "Limpar filtros" para resetar

#### Ordenação
Ordene os estudantes por:
- Nome (A-Z)
- Idade (crescente/decrescente)
- Escolaridade
- Taxa de Conclusão (%)

#### Detalhes do Estudante
- Clique em qualquer card de estudante
- Veja todos os conteúdos organizados por tipo
- Veja status de conclusão e datas

### 📊 Dados Mockados

Os dados estão em `public/students.json`:
- 40 estudantes
- Idades: 10-28 anos
- 3 níveis de escolaridade
- 5-15 conteúdos por estudante
- 3 tipos de conteúdo (vídeo, atividade, exercício)
- 3 níveis de dificuldade (Fácil, Médio, Difícil)

### 🛠️ Comandos Disponíveis

```bash
# Desenvolvimento
npm run dev          # Inicia servidor local na porta 3000

# Produção
npm run build        # Cria build otimizado
npm run start        # Inicia servidor de produção

# Linting (se configurado)
npm run lint         # Verifica código
```

### 📱 Responsividade

O dashboard é totalmente responsivo:
- **Mobile**: Design otimizado para celular
- **Tablet**: Layout adaptado para tablets
- **Desktop**: Experiência completa em tela grande

### 🎯 Personalização

#### Modificar Dados
Edite `public/students.json` para adicionar/remover estudantes

#### Alterar Cores
Edite `tailwind.config.js` para personalizar o tema

#### Adicionar Funcionalidades
Os componentes estão em `components/`:
- Todos em TypeScript
- Totalmente tipados
- Fácil de estender

### 📚 Estrutura de Arquivos

```
dashboard/
├── components/          # Componentes React
│   ├── charts/         # Gráficos (Recharts)
│   └── ...             # Outros componentes
├── pages/              # Páginas Next.js
├── public/             # Arquivos estáticos
│   └── students.json   # Dados mockados
├── styles/             # CSS global
├── types/              # TypeScript types
└── utils/              # Funções auxiliares
```

### 🐛 Troubleshooting

**Porta 3000 em uso?**
```bash
# Use outra porta
PORT=3001 npm run dev
```

**Erro ao instalar dependências?**
```bash
# Limpe o cache e reinstale
rm -rf node_modules package-lock.json
npm install
```

**Build falhando?**
```bash
# Verifique a versão do Node (recomendado: 18+)
node --version

# Limpe o cache do Next.js
rm -rf .next
npm run build
```

### 📖 Mais Informações

Veja o `README.md` para documentação completa!

### ✨ Pronto!

Seu dashboard está rodando e pronto para uso! 🎉

