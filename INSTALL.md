# Instalação por ferramenta

O pacote é uma pasta de markdown + JSON. Cada assistente tem um lugar próprio onde procura esse tipo
de arquivo — abaixo, o caminho certo de cada um.

Clone uma vez:

```bash
git clone https://github.com/thiagojbs/flwchat-api-kb.git
```

---

## Claude Code

Skills pessoais ficam em `~/.claude/skills/<nome>/` e valem em **todos** os seus projetos.
Basta a pasta ter um `SKILL.md` com frontmatter — o nosso já tem.

```bash
cp -R flwchat-api-kb ~/.claude/skills/flwchat-api
```

Só para um projeto (e versionado junto com o código do time):

```bash
mkdir -p .claude/skills && cp -R ~/flwchat-api-kb .claude/skills/flwchat-api
```

Skill de projeto tem precedência sobre a pessoal de mesmo nome. Confira com `/skills` dentro da sessão;
o Claude carrega sozinho quando o assunto é a API — não precisa citar o arquivo.

## Codex CLI (ChatGPT)

O Codex lê `AGENTS.md` do git root até o diretório atual, e o global em `~/.codex/AGENTS.md`.
Ele **não** varre pastas sozinho: é preciso apontar o caminho.

Para todos os seus projetos:

```bash
git clone https://github.com/thiagojbs/flwchat-api-kb.git ~/.codex/flwchat-api-kb
cat >> ~/.codex/AGENTS.md <<'EOF'

## API flw.chat / wts.chat
Ao trabalhar com essa API, leia primeiro ~/.codex/flwchat-api-kb/SKILL.md.
Base URL: https://api.wts.chat/{core|chat|crm} — o prefixo de serviço é obrigatório.
Campos de cada endpoint em reference/, specs OpenAPI em openapi/.
EOF
```

Para um projeto só: clone em `vendor/flwchat-api-kb` e coloque o mesmo bloco no `AGENTS.md` do repositório,
trocando o caminho. Confira o que foi carregado com `codex --print-instructions`.

## Cursor

```bash
mkdir -p .cursor/rules && cp -R ~/flwchat-api-kb .cursor/flwchat-api-kb
cat > .cursor/rules/flwchat-api.mdc <<'EOF'
---
description: API flw.chat / wts.chat
globs:
alwaysApply: false
---
Consulte .cursor/flwchat-api-kb/SKILL.md antes de escrever qualquer chamada à API flw.chat.
Base URL: https://api.wts.chat/{core|chat|crm}.
EOF
```

Ou, mais simples: deixe a pasta no repositório e use `@flwchat-api-kb/SKILL.md` no chat.

## GitHub Copilot

```bash
cp -R ~/flwchat-api-kb docs/flwchat-api-kb
mkdir -p .github && cat >> .github/copilot-instructions.md <<'EOF'

## API flw.chat
Referência em docs/flwchat-api-kb/SKILL.md. Base URL https://api.wts.chat/{core|chat|crm}.
EOF
```

## ChatGPT / Claude / Gemini pelo navegador

Sem instalação — anexe o arquivo à conversa:

- `llms-full.md` (376 KB, ~94k tokens) — tudo: guias + referência completa.
- `SKILL.md` (24 KB) — só o essencial, quando a janela for curta ou o plano limitar anexo.

Em Projects/GPTs personalizados, suba `llms-full.md` uma vez na base de conhecimento e todas as
conversas daquele projeto passam a ter a API.

## Postman

`File > Import` e selecione os três arquivos de `postman/`. Em cada coleção, aba **Variables**,
preencha `token` com o seu `pn_...`. O `baseUrl` já vem preenchido por serviço.

---

## Conferindo se funcionou

Peça: **"qual a base URL da API flw.chat e como envio um template?"**

Resposta certa cita `https://api.wts.chat/chat/v1/send/template` e menciona que no WhatsApp a conversa
só pode ser iniciada com template. Se vier `api.flw.chat/v1/...`, o arquivo não foi carregado.

## Token

Cada pessoa gera o seu em `Ajustes > Integrações > Integração via API`. Guarde em variável de ambiente
(`FLW_TOKEN`), nunca em código — este repositório é público.
