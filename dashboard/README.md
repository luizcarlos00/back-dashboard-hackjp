# Dashboard (Next.js)

Projeto Next.js inicializado dentro da pasta `dashboard`.

Como usar

1. Instalar dependências (pnpm):

```bash
pnpm install
```

2. Rodar em modo desenvolvimento:

```bash
pnpm dev
```

3. Criar build de produção e iniciar:

```bash
pnpm build
pnpm start
```

Observações

- Dependências: `next`, `react`, `react-dom`.
- Esta é uma configuração mínima. Adapte conforme necessário.

Dados e dashboard

- O dashboard carrega dados de `public/data.json` por padrão. Edite esse arquivo para testar outros conjuntos de dados.
- Estrutura esperada (exemplo de cada item):

```json
{ "id": 1, "name": "Projeto Alpha", "value": 120, "category": "A", "date": "2025-10-01" }
```

- Após alterar `public/data.json` basta recarregar a página do navegador em modo desenvolvimento.

Se quiser usar outras bibliotecas gráficas (Chart.js, Recharts etc.), instale via `pnpm add` e adapte `pages/index.js`.
