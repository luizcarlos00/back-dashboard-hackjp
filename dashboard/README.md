# Dashboard Estudantil Interativo

Dashboard moderno e minimalista desenvolvido com Next.js, TypeScript e Tailwind CSS para visualização e análise de dados de estudantes.

## 🚀 Características

### Design & UX
- ✨ Interface minimalista e moderna
- 🌓 Dark mode completo
- 📱 Totalmente responsivo (mobile-first)
- 🎨 Paleta de cores profissional com gradientes
- ⚡ Animações e transições suaves
- 🎯 Componentes reutilizáveis e modulares

### Funcionalidades

#### Dashboard Principal
- **Estatísticas Gerais**: Cards com métricas agregadas
- **Gráficos Interativos**:
  - Distribuição por dificuldade (Pizza)
  - Top 10 estudantes por taxa de conclusão (Barras)
  - Conteúdos por tipo (Barras)

#### Filtros Avançados
- 🔍 Busca por nome
- 👥 Faixa etária (slider duplo)
- 🎓 Nível de escolaridade
- 📊 Tipo de conteúdo
- 🎯 Nível de dificuldade

#### Ordenação
- Nome
- Idade
- Escolaridade
- Taxa de conclusão

#### Detalhes do Estudante
- Modal completo com informações detalhadas
- Lista de conteúdos organizados por tipo
- Indicadores de conclusão
- Badges de dificuldade
- Datas de início

## 🛠️ Tecnologias

- **Next.js 16** - Framework React
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Estilização
- **Recharts** - Gráficos interativos
- **Headless UI** - Componentes acessíveis
- **Lucide React** - Ícones modernos

## 📦 Instalação

```bash
# Instalar dependências
npm install

# Iniciar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Iniciar produção
npm start
```

O dashboard estará disponível em [http://localhost:3000](http://localhost:3000)

## 📁 Estrutura do Projeto

```
dashboard/
├── components/
│   ├── charts/
│   │   ├── DifficultyDistribution.tsx
│   │   ├── ProgressOverview.tsx
│   │   └── ContentTypeChart.tsx
│   ├── DashboardStats.tsx
│   ├── Filters.tsx
│   ├── Header.tsx
│   ├── Layout.tsx
│   ├── StudentCard.tsx
│   ├── StudentDetailModal.tsx
│   └── ThemeProvider.tsx
├── pages/
│   ├── _app.tsx
│   └── index.tsx
├── public/
│   └── students.json
├── styles/
│   └── globals.css
├── types/
│   └── index.ts
├── utils/
│   └── mockData.ts
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## 📊 Modelo de Dados

### Student (Estudante)
```typescript
{
  id: number
  nome: string
  idade: number
  escolaridade: "Fundamental" | "Médio" | "Superior"
  conteudos: Content[]
}
```

### Content (Conteúdo)
```typescript
{
  id: string
  tipo: "video" | "atividade" | "exercicio"
  titulo: string
  dificuldade: "Fácil" | "Médio" | "Difícil"
  concluido: boolean
  dataInicio?: string
}
```

## 🎨 Personalização

### Cores (Tailwind)
As cores podem ser customizadas em `tailwind.config.js`. O tema atual usa:
- **Primary**: Indigo/Purple
- **Success**: Green
- **Warning**: Amber
- **Danger**: Red

### Dark Mode
O dark mode é implementado usando a estratégia `class` do Tailwind e pode ser alternado através do botão no header.

### Dados
Para alterar os dados mockados, edite o arquivo `public/students.json` ou modifique o gerador em `utils/mockData.ts`.

## 🔧 Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run start` - Inicia servidor de produção

## 📝 Melhorias Futuras

- [ ] Exportação de dados (CSV, PDF)
- [ ] Gráficos adicionais (linha do tempo, mapa de calor)
- [ ] Filtros salvos/favoritos
- [ ] Comparação entre estudantes
- [ ] Modo de impressão
- [ ] API Backend real
- [ ] Autenticação de usuários
- [ ] Notificações push

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Desenvolvimento

Desenvolvido com ❤️ usando Next.js, TypeScript e Tailwind CSS.
