# AGENTS.md

Este repositório é um pacote de conhecimento da API **flw.chat / wts.chat**, não uma aplicação.

- Comece por `SKILL.md` — base URL, auth, rate limits, erros e o índice das 109 rotas.
- Campos de cada endpoint: `reference/<domínio>.md`. Specs: `openapi/{core,chat,crm}.json`.
- Base URL é `https://api.wts.chat/{core|chat|crm}`; o prefixo de serviço é obrigatório.
- Conteúdo é **gerado** por `build.py` a partir de https://flwchat.readme.io. Não edite
  `reference/`, `openapi/`, `guides/`, `llms-full.md` nem `index.json` à mão — a próxima build
  sobrescreve. Texto curado só no `SKILL.md`, fora do bloco `<!-- ENDPOINTS:START/END -->`.
