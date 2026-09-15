# flwchat-api-kb

Documentação da API **flw.chat / wts.chat** empacotada para ser lida por IA — Claude, ChatGPT/Codex,
Cursor, Copilot — e por ferramentas (Postman, geradores de cliente).

Fonte: <https://flwchat.readme.io> · **109 endpoints** em 3 serviços · scrape de **2026-09-15**.

## O que tem aqui

| Arquivo | Para quê | Tamanho |
|---|---|---|
| `SKILL.md` | **Comece aqui.** Base URL, auth, rate limits, erros, qual endpoint de envio usar, fluxo de arquivo, webhooks + índice das 109 rotas | 24 KB |
| `reference/*.md` | 19 arquivos por domínio: todo campo de todo endpoint (tipo, obrigatoriedade, descrição, enums) + schemas | 340 KB |
| `openapi/{core,chat,crm}.json` | Specs OpenAPI 3.0.1 completos — fonte de verdade para codegen | 536 KB |
| `postman/*.postman_collection.json` | Coleções prontas; preencha a variável `token` | 1,7 MB |
| `guides/*.md` | As 16 páginas conceituais e tutoriais originais (auth, paginação, rate limit, webhooks, UTM, N8N, MAKE, firewall) | 80 KB |
| `llms-full.md` | Tudo num arquivo só (~94k tokens) para colar em janela de contexto | 376 KB |
| `index.json` | As 109 operações em JSON (método, path, resumo, tag, página de origem) | 33 KB |

## Para o time — instalação em 1 minuto

```bash
git clone https://github.com/thiagojbs/flwchat-api-kb.git
cp -R flwchat-api-kb ~/.claude/skills/flwchat-api   # Claude Code: carrega sozinho
```

Depois disso, basta pedir em linguagem natural ("manda um template pelo flw.chat para esse número")
que o Claude já sabe a base URL, a auth e o payload — sem consultar o site.

Não usa Claude Code? Escolha um:

| Ferramenta | O que fazer |
|---|---|
| ChatGPT / Gemini | anexar `llms-full.md` à conversa (ou colar `SKILL.md`, que é menor) |
| Cursor / Copilot / Windsurf | clonar a pasta dentro do repositório do projeto |
| Postman | importar `postman/*.postman_collection.json` e preencher a variável `token` |
| Qualquer IA, sem clonar | colar a URL: https://raw.githubusercontent.com/thiagojbs/flwchat-api-kb/main/SKILL.md |

**Cada pessoa usa o próprio token** (`Ajustes > Integrações > Integração via API`). Nunca comite um
`pn_...` aqui — o repositório é público.

Quando a flw.chat mudar a documentação, quem rodar `python3 build.py --no-cache` e der push atualiza
o time inteiro; o `git diff` mostra exatamente o que mudou na API.

## Como usar

**Claude Code** — copie a pasta para dentro do projeto e aponte o `CLAUDE.md` para `SKILL.md`, ou
instale como skill global:

```bash
cp -R . ~/.claude/skills/flwchat-api
```

O frontmatter de `SKILL.md` já traz `name` e `description`, então o Claude carrega sozinho quando o
assunto é a API.

**ChatGPT / Gemini / qualquer chat** — suba `llms-full.md` como arquivo, ou cole o `SKILL.md`
(24 KB) quando a janela for curta.

**Cursor / Copilot / Windsurf** — deixe a pasta no repositório; o `SKILL.md` e o `reference/` são
indexados junto com o código.

**Postman** — importe `postman/*.postman_collection.json` e preencha a variável `token` com
`pn_...` (a coleção já usa auth Bearer herdada por todos os requests).

**Gerar um cliente** — os specs são OpenAPI 3.0.1 válidos:

```bash
npx @openapitools/openapi-generator-cli generate -i openapi/chat.json -g typescript-fetch -o ./sdk-chat
```

## Atualizar

```bash
python3 build.py            # usa o cache local em .cache/
python3 build.py --no-cache # rebaixa as 125 páginas
```

O script baixa `llms.txt`, extrai o OpenAPI embutido em cada página, mescla por serviço e regera
`openapi/`, `reference/`, `guides/`, `llms-full.md`, `index.json`, `postman/` e o índice de endpoints
dentro do `SKILL.md` (só o bloco entre `<!-- ENDPOINTS:START/END -->`; o texto escrito à mão é preservado).

Só stdlib do Python 3 — `npx` é opcional e usado apenas para as coleções Postman.

Checagens que fazem o build falhar se a documentação mudar de forma inesperada:

- colisão de schema de mesmo nome com conteúdo diferente (renomeia por hash e lista os conflitos);
- operação `(método, path)` duplicada entre páginas;
- nº de operações mescladas menor que o nº de páginas de endpoint;
- nº de operações renderizadas em `reference/` diferente do total.

## Armadilhas que este pacote existe para evitar

1. **A base URL é `https://api.wts.chat/{core|chat|crm}`** — com o prefixo de serviço. `api.flw.chat`
   é alias válido do mesmo backend, mas o exemplo de curl do guia oficial "Criar token" mostra
   `api.flw.chat/v1/channel`, sem prefixo, e isso responde `400 badrequest`.
2. **Dois regimes de rate limit**: 1000/5min + burst 200/5s na API em geral, e 1000/2min próprios da
   família `/chat/v1/send/*`.
3. **Status de mensagem e status de OTP usam enums diferentes.**
4. **No WhatsApp, conversa só pode ser iniciada com template** — `send/text` é recusado sem conversa aberta.
5. Rota inexistente sem token devolve `401`, não `404`.

## Licença

Conteúdo derivado da documentação pública da flw.chat, para uso interno nas integrações.
`build.py` é o único código original aqui.
