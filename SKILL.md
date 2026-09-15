---
name: flwchat-api
description: API flw.chat / wts.chat (atendimento WhatsApp, Instagram, Messenger) - autenticacao, rate limits, envio de mensagens e templates, contatos, conversas, chatbots, webhooks, CRM. Use ao integrar, depurar ou gerar codigo para qualquer endpoint api.wts.chat.
---

# API flw.chat — referência rápida

> Gerado de https://flwchat.readme.io (109 endpoints, 3 serviços). Specs completos em `openapi/`.

## ⚠️ Base URL (erro nº 1)

```
https://api.wts.chat/{core|chat|crm}/{versão}/{recurso}
```

- **O prefixo de serviço é obrigatório.** `https://api.wts.chat/v1/channel` → `400 badrequest`.
  O correto é `https://api.wts.chat/chat/v1/channel`.
- `api.flw.chat` é alias válido do mesmo backend (também exige o prefixo), mas **`api.wts.chat` é o host
  canônico** — é o que está nos specs. *(Verificado por requisição real em 2026-09-15; o exemplo de
  curl do guia "Criar token" mostra `api.flw.chat/v1/channel`, que está errado — não copie de lá.)*
- Nunca invente `api.flw.chat/v1/...` nem `flwchat.readme.io` como host de API.

| Serviço | Base | O que vive aqui |
|---|---|---|
| `core` | `https://api.wts.chat/core` | contatos, etiquetas, campos personalizados, usuários, equipes, carteiras, arquivos, webhooks, horário de atendimento |
| `chat` | `https://api.wts.chat/chat` | conversas, mensagens, envios, templates, chatbots, canais, sequências, mensagens agendadas |
| `crm`  | `https://api.wts.chat/crm`  | painéis (funis), cards, anotações, motivos de perda |

## Autenticação

Token permanente gerado em `Ajustes > Integrações > Integração via API`. Em **toda** requisição:

```
Authorization: Bearer pn_xxxxxxxxxxxxxxxxxxxxxx
```

Sem `Bearer`, ou com token inválido/revogado → `401` com `key: ERROR_UNAUTHORIZED`.

## Paginação

Listagens usam `pageNumber` e `pageSize` (**máx. 100**) — query string nos `GET`, corpo nos `POST /filter`.
Mantenha `pageSize` constante ao iterar, senão `pageNumber` devolve resultados deslocados.

```jsonc
// resposta
{ "pageNumber": 1, "pageSize": 50, "totalPages": 5, "totalItems": 250,
  "hasMorePages": true, "items": [ /* ... */ ] }
```

Itere enquanto `hasMorePages === true`.

## Rate limiting — dois regimes distintos

| Escopo | Limite |
|---|---|
| API em geral (por conta) | **1.000 req / 5 min** + burst **200 req / 5 s** |
| Família `POST/GET /chat/v1/send/*` | **1.000 req / 2 min** (limite próprio, independente) |

Excedeu → `429 Too Many Requests`. Implemente backoff exponencial; não repita imediatamente.

## Envelope de erro

Todos os erros (4xx e 5xx) voltam nesta forma — guarde `id.shortValue` para abrir suporte:

```json
{ "id": { "value": "c44bf0cc-...", "shortValue": "c44bf0cc" },
  "httpStatusCode": 401, "error": true, "date": "2026-09-15T19:41:56Z",
  "key": "ERROR_UNAUTHORIZED", "text": "Acesso negado", "isUnsolvableError": false }
```

Nos specs aparece como `InternalException`; `ProblemDetails` (RFC 7807) é o formato de validação em alguns 400.
**Atenção:** rota inexistente sem token retorna `401`, não `404` — a autenticação roda antes do roteamento.

## Convenções

- **Telefone**: `+55|11999999999` (DDI, pipe, número sem máscara) — formato de `phonenumber`.
- `to` = número de telefone **ou** `@usuarioinstagram` do destinatário. `from` = número/`@usuario` do
  **canal** da conta que envia (liste em `GET /chat/v1/channel`); omitido, a plataforma resolve o canal.
- **IDs**: UUID v4. **Datas**: ISO-8601 UTC (`2026-09-15T19:41:56.925079Z`).
- `senderId`: seu ID próprio, opcional em qualquer envio — serve para rastrear a mensagem depois sem guardar o ID da plataforma.
- `sessionMetadata`: chave-valor livre, acessível como variável no chatbot e devolvido nos webhooks.

## Qual endpoint de envio usar

São **três superfícies sobrepostas**. Regra prática:

| Situação | Use |
|---|---|
| Disparo novo (padrão, use este) | `POST /chat/v1/send/{text,image,audio,video,document,template,otp,typing}` |
| Responder dentro de uma conversa que você já tem o ID | `POST /chat/v1/session/{id}/message` |
| Envio genérico legado (payload polimórfico) | `POST /chat/v1/message/send` |
| Lote (até 100 destinatários) | `POST /chat/v1/send/template/batch` · `POST /chat/v1/send/chatbot/batch` |
| Precisa do status **na mesma chamada** | variantes `/sync` (`/chat/v1/message/send-sync`, `/chat/v1/session/{id}/message/sync`) — teto de **25 s** |

**Regras que valem para todos os envios:**

1. **No WhatsApp, conversa só pode ser *iniciada* com template** (regra repetida em todos os endpoints de envio).
   Sem conversa aberta, `POST /chat/v1/send/text` é recusado — use `POST /chat/v1/send/template` com um
   `templateId` de `GET /chat/v1/template` e `parameters` preenchido. Texto livre só depois que o contato
   responde (janela de atendimento do WhatsApp, 24 h).
2. **Contato inexistente é criado automaticamente** antes do envio. Não precisa criar antes.
3. Envio é **assíncrono** por padrão: a resposta traz `id` e `status` inicial, não a entrega.
   Acompanhe por `GET /chat/v1/send/message/{id}` (ou `GET /chat/v1/message/{id}/status`), ou passe
   `callbackUrl` no corpo e receba o webhook de entrega/falha.
   `status` de mensagem ∈ `PROCESSING | SAVED | QUEUED | SENT | DELIVERED | READ | FAILED | DELETED | WAIT_REPLY`;
   falha explica em `failedReason`. **OTP usa outro enum**: `UNDEFINED | PENDING | SENT | RECEIVED | FAILED`
   (consulta em `GET /chat/v1/send/otp/{id}`, que aceita o ID da mensagem **ou** o seu `senderId`).
4. `options` controla o atendimento criado: `enableBot`, `hiddenSession`, `forceStartSession`, `user`, `department`.
5. `delayTyping` (≤ 25 s) simula "digitando" antes de entregar. Em canal CloudAPI oficial prefira
   `POST /chat/v1/send/typing`.
6. `refId` responde a uma mensagem específica (reply).

## Enviar arquivo — 3 passos

`fileIdOrUrl` aceita **URL pública** (caminho curto, nada a fazer) ou um **FileId** da plataforma.
Para o FileId, que é reutilizável indefinidamente:

```bash
# 1. pede a URL de upload (Type: UNDEFINED|PDF|EXCEL|WORD|IMAGE|AUDIO|VIDEO|DOCUMENT)
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.wts.chat/core/v2/file?Type=IMAGE&Name=foto.jpg&MimeType=image/jpeg"
# -> { "tempFileId": "...", "urlUpload": "https://..." }

# 2. sobe o conteúdo com PUT na urlUpload (sem header de Authorization)
curl -X PUT --upload-file foto.jpg "$URL_UPLOAD"

# 3. confirma e recebe o FileId definitivo
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"tempFileId":"..."}' https://api.wts.chat/core/v2/file
# -> { "id": "FILE_ID", "name": ..., "mimeType": ..., "size": ... }
```

`IMAGE` e `VIDEO` passam por transformação/compressão para compatibilidade entre canais; `DOCUMENT` não.

## Webhooks

Assine por API (`POST /core/v1/webhook/subscription`) ou em `Ajustes > Integrações > Webhooks`.
A plataforma faz `POST` na sua URL pública com:

```json
{ "eventType": "CONTACT_UPDATE", "date": "2026-09-15T16:42:35.4359934Z", "content": { } }
```

Eventos assináveis (enum fixo, de `GET /core/v1/webhook/event`):

```
SESSION_NEW  SESSION_UPDATE  SESSION_COMPLETE
MESSAGE_RECEIVED  MESSAGE_UPDATED  MESSAGE_SENT
CONTACT_NEW  CONTACT_UPDATE  CONTACT_TAG_UPDATE
PAYMENT_NEW  PAYMENT_UPDATE
PANEL_CARD_NEW  PANEL_CARD_UPDATE  PANEL_CARD_STEP_CHANGE
PANEL_CARD_NOTE_NEW  PANEL_CARD_NOTE_UPDATE
```

Assinatura pode ser desativada (pausa) sem ser removida. `callbackUrl` nos envios é um webhook
pontual por mensagem, independente das assinaturas.

## Exemplo mínimo

```bash
# template (único jeito de iniciar conversa no WhatsApp)
curl -X POST https://api.wts.chat/chat/v1/send/template \
  -H "Authorization: Bearer $FLW_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "to": "+55|11999999999",
    "templateId": "UUID_DO_TEMPLATE",
    "parameters": { "1": "João", "2": "12345" },
    "senderId": "pedido-9876",
    "options": { "enableBot": true }
  }'
```

## Onde achar o resto

- `reference/*.md` — 19 arquivos por domínio: todo campo de todo endpoint, com tipo, obrigatoriedade,
  descrição e enums, mais os schemas usados. É onde olhar antes de montar um payload.
- `openapi/{core,chat,crm}.json` — specs completos. Fonte de verdade para codegen/Postman.
- `llms-full.md` — tudo acima num arquivo só, para colar em janela de contexto.
- `guides/` — páginas conceituais e tutoriais originais (auth, paginação, rate limit, webhooks, UTM, N8N, MAKE, firewall, login integrado).
- `index.json` — as 109 operações em JSON (método, path, resumo, tag, página de origem).
- `python3 build.py` regenera tudo da documentação publicada.

## Índice de endpoints

Paths abaixo já incluem o prefixo de serviço — cole direto após `https://api.wts.chat`.

<!-- ENDPOINTS:START -->

### CORE — `https://api.wts.chat/core`

**Arquivos**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v2/file` | Obter url para upload | [↗](https://flwchat.readme.io/reference/get_v2-file) |
| `POST` | `/core/v2/file` | Salvar arquivo | [↗](https://flwchat.readme.io/reference/post_v2-file) |

**Campos**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/custom-field` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-custom-field) |

**Carteiras**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/portfolio` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-portfolio) |
| `DELETE` | `/core/v1/portfolio/{id}/contact` | Remover contato | [↗](https://flwchat.readme.io/reference/delete_v1-portfolio-id-contact) |
| `GET` | `/core/v1/portfolio/{id}/contact` | Listar contatos | [↗](https://flwchat.readme.io/reference/get_v1-portfolio-id-contact) |
| `POST` | `/core/v1/portfolio/{id}/contact` | Adicionar contato | [↗](https://flwchat.readme.io/reference/post_v1-portfolio-id-contact) |
| `DELETE` | `/core/v1/portfolio/{id}/contact/batch` | Remover contatos | [↗](https://flwchat.readme.io/reference/delete_v1-portfolio-id-contact-batch) |
| `POST` | `/core/v1/portfolio/{id}/contact/batch` | Adicionar contatos | [↗](https://flwchat.readme.io/reference/post_v1-portfolio-id-contact-batch) |

**Contatos**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/contact` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-contact) |
| `POST` | `/core/v1/contact` | Criar | [↗](https://flwchat.readme.io/reference/post_v1-contact) |
| `GET` | `/core/v1/contact/custom-field` | Campos personalizados | [↗](https://flwchat.readme.io/reference/get_v1-contact-custom-field) |
| `POST` | `/core/v1/contact/filter` | Filtrar | [↗](https://flwchat.readme.io/reference/post_v1-contact-filter) |
| `GET` | `/core/v1/contact/phonenumber/{phone}` | Obter por Número de telefone | [↗](https://flwchat.readme.io/reference/get_v1-contact-phonenumber-phone) |
| `PUT` | `/core/v1/contact/phonenumber/{phone}` | Atualizar por Número de telefone | [↗](https://flwchat.readme.io/reference/put_v1-contact-phonenumber-phone) |
| `POST` | `/core/v1/contact/phonenumber/{phone}/tags` | Atualizar etiquetas por Número de telefone | [↗](https://flwchat.readme.io/reference/post_v1-contact-phonenumber-phone-tags) |
| `GET` | `/core/v1/contact/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-contact-id) |
| `POST` | `/core/v1/contact/{id}/tags` | Atualizar etiquetas | [↗](https://flwchat.readme.io/reference/post_v1-contact-id-tags) |
| `POST` | `/core/v2/contact/batch` | Salvar em massa | [↗](https://flwchat.readme.io/reference/post_v2-contact-batch) |
| `PUT` | `/core/v2/contact/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v2-contact-id) |

**Equipes**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `POST` | `/core/v1/department` | Criar | [↗](https://flwchat.readme.io/reference/post_v1-department) |
| `DELETE` | `/core/v1/department/{id}` | Excluir | [↗](https://flwchat.readme.io/reference/delete_v1-department-id) |
| `GET` | `/core/v1/department/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-department-id) |
| `PUT` | `/core/v1/department/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v1-department-id) |
| `PUT` | `/core/v1/department/{id}/agents` | Atualizar usuários | [↗](https://flwchat.readme.io/reference/put_v1-department-id-agents) |
| `GET` | `/core/v1/department/{id}/channel` | Listar canais | [↗](https://flwchat.readme.io/reference/get_v1-department-id-channel) |
| `GET` | `/core/v2/department` | Listar | [↗](https://flwchat.readme.io/reference/get_v2-department) |

**Etiquetas**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/tag` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-tag) |
| `POST` | `/core/v1/tag` | Criar | [↗](https://flwchat.readme.io/reference/post_v1-tag) |
| `GET` | `/core/v1/tag/color` | Listar cores | [↗](https://flwchat.readme.io/reference/get_v1-tag-color) |
| `DELETE` | `/core/v1/tag/{id}` | Excluir | [↗](https://flwchat.readme.io/reference/delete_v1-tag-id) |
| `PUT` | `/core/v1/tag/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v1-tag-id) |

**Horários de Atendimento**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/company/officehours` | Obter | [↗](https://flwchat.readme.io/reference/get_v1-company-officehours) |

**Usuários**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/agent` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-agent) |
| `POST` | `/core/v1/agent` | Criar | [↗](https://flwchat.readme.io/reference/post_v1-agent) |
| `DELETE` | `/core/v1/agent/{id}` | Excluir | [↗](https://flwchat.readme.io/reference/delete_v1-agent-id) |
| `GET` | `/core/v1/agent/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-agent-id) |
| `PUT` | `/core/v1/agent/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v1-agent-id) |
| `POST` | `/core/v1/agent/{id}/departments` | Atualizar equipes | [↗](https://flwchat.readme.io/reference/post_v1-agent-id-departments) |
| `POST` | `/core/v1/agent/{id}/logout` | Fazer logout | [↗](https://flwchat.readme.io/reference/post_v1-agent-id-logout) |
| `POST` | `/core/v1/agent/{id}/status` | Alterar status | [↗](https://flwchat.readme.io/reference/post_v1-agent-id-status) |

**Webhooks**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/core/v1/webhook/event` | Listar eventos | [↗](https://flwchat.readme.io/reference/get_v1-webhook-event) |
| `GET` | `/core/v1/webhook/subscription` | Listar assinaturas | [↗](https://flwchat.readme.io/reference/get_v1-webhook-subscription) |
| `POST` | `/core/v1/webhook/subscription` | Cria assinatura | [↗](https://flwchat.readme.io/reference/post_v1-webhook-subscription) |
| `DELETE` | `/core/v1/webhook/subscription/{subscriptionId}` | Remove assinatura | [↗](https://flwchat.readme.io/reference/delete_v1-webhook-subscription-subscriptionid) |
| `GET` | `/core/v1/webhook/subscription/{subscriptionId}` | Busca assinatura por ID | [↗](https://flwchat.readme.io/reference/get_v1-webhook-subscription-subscriptionid) |
| `PUT` | `/core/v1/webhook/subscription/{subscriptionId}` | Atualiza assinatura | [↗](https://flwchat.readme.io/reference/put_v1-webhook-subscription-subscriptionid) |


### CHAT — `https://api.wts.chat/chat`

**Canais de Atendimento**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/channel` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-channel) |

**Chatbots**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/chatbot` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-chatbot) |
| `POST` | `/chat/v1/chatbot/send` | Enviar chatbot | [↗](https://flwchat.readme.io/reference/post_v1-chatbot-send) |

**Conversas**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `DELETE` | `/chat/v1/session/note/{id}` | Excluir uma nota interna | [↗](https://flwchat.readme.io/reference/delete_v1-session-note-id) |
| `GET` | `/chat/v1/session/note/{id}` | Obter uma nota interna | [↗](https://flwchat.readme.io/reference/get_v1-session-note-id) |
| `PUT` | `/chat/v1/session/{id}/assignee` | Atribuir usuário | [↗](https://flwchat.readme.io/reference/put_v1-session-id-assignee) |
| `PUT` | `/chat/v1/session/{id}/complete` | Concluir | [↗](https://flwchat.readme.io/reference/put_v1-session-id-complete) |
| `GET` | `/chat/v1/session/{id}/message` | Listar mensagens | [↗](https://flwchat.readme.io/reference/get_v1-session-id-message) |
| `POST` | `/chat/v1/session/{id}/message` | Enviar mensagem | [↗](https://flwchat.readme.io/reference/post_v1-session-id-message) |
| `POST` | `/chat/v1/session/{id}/message/sync` | Enviar mensagem síncrona | [↗](https://flwchat.readme.io/reference/post_v1-session-id-message-sync) |
| `GET` | `/chat/v1/session/{id}/note` | Listar notas internas | [↗](https://flwchat.readme.io/reference/get_v1-session-id-note) |
| `POST` | `/chat/v1/session/{id}/note` | Salvar nota interna | [↗](https://flwchat.readme.io/reference/post_v1-session-id-note) |
| `PUT` | `/chat/v1/session/{id}/status` | Alterar status | [↗](https://flwchat.readme.io/reference/put_v1-session-id-status) |
| `PUT` | `/chat/v1/session/{id}/transfer` | Transferir | [↗](https://flwchat.readme.io/reference/put_v1-session-id-transfer) |
| `GET` | `/chat/v2/session` | Listar | [↗](https://flwchat.readme.io/reference/get_v2-session) |
| `GET` | `/chat/v2/session/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v2-session-id) |
| `PUT` | `/chat/v2/session/{id}/partial` | Alterar | [↗](https://flwchat.readme.io/reference/put_v2-session-id-partial) |

**Envios (Msg/Otp/Bot)**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `POST` | `/chat/v1/send/audio` | Áudio | [↗](https://flwchat.readme.io/reference/post_v1-send-audio) |
| `POST` | `/chat/v1/send/chatbot` | Chatbot | [↗](https://flwchat.readme.io/reference/post_v1-send-chatbot) |
| `POST` | `/chat/v1/send/chatbot/batch` | Chatbot (em lote) | [↗](https://flwchat.readme.io/reference/post_v1-send-chatbot-batch) |
| `GET` | `/chat/v1/send/chatbot/{id}` | Chatbot status | [↗](https://flwchat.readme.io/reference/get_v1-send-chatbot-id) |
| `POST` | `/chat/v1/send/document` | Documento | [↗](https://flwchat.readme.io/reference/post_v1-send-document) |
| `POST` | `/chat/v1/send/image` | Imagem | [↗](https://flwchat.readme.io/reference/post_v1-send-image) |
| `GET` | `/chat/v1/send/message/{id}` | Mensagem status | [↗](https://flwchat.readme.io/reference/get_v1-send-message-id) |
| `POST` | `/chat/v1/send/otp` | OTP | [↗](https://flwchat.readme.io/reference/post_v1-send-otp) |
| `GET` | `/chat/v1/send/otp/{id}` | OTP status | [↗](https://flwchat.readme.io/reference/get_v1-send-otp-id) |
| `POST` | `/chat/v1/send/template` | Modelo | [↗](https://flwchat.readme.io/reference/post_v1-send-template) |
| `POST` | `/chat/v1/send/template/batch` | Modelo (em lote) | [↗](https://flwchat.readme.io/reference/post_v1-send-template-batch) |
| `POST` | `/chat/v1/send/text` | Texto | [↗](https://flwchat.readme.io/reference/post_v1-send-text) |
| `POST` | `/chat/v1/send/typing` | Digitando | [↗](https://flwchat.readme.io/reference/post_v1-send-typing) |
| `POST` | `/chat/v1/send/video` | Vídeo | [↗](https://flwchat.readme.io/reference/post_v1-send-video) |

**Mensagens**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/message` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-message) |
| `POST` | `/chat/v1/message/send` | Enviar | [↗](https://flwchat.readme.io/reference/post_v1-message-send) |
| `POST` | `/chat/v1/message/send-sync` | Enviar síncrono | [↗](https://flwchat.readme.io/reference/post_v1-message-send-sync) |
| `DELETE` | `/chat/v1/message/{id}` | Excluir mensagem | [↗](https://flwchat.readme.io/reference/delete_v1-message-id) |
| `GET` | `/chat/v1/message/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-message-id) |
| `GET` | `/chat/v1/message/{id}/status` | Obter status por ID | [↗](https://flwchat.readme.io/reference/get_v1-message-id-status) |

**Mensagens Agendadas**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/scheduled-message` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-scheduled-message) |
| `POST` | `/chat/v1/scheduled-message` | Criar | [↗](https://flwchat.readme.io/reference/post_v1-scheduled-message) |
| `POST` | `/chat/v1/scheduled-message/batch-cancel` | Cancelar em massa | [↗](https://flwchat.readme.io/reference/post_v1-scheduled-message-batch-cancel) |
| `GET` | `/chat/v1/scheduled-message/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-scheduled-message-id) |
| `PUT` | `/chat/v1/scheduled-message/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v1-scheduled-message-id) |
| `POST` | `/chat/v1/scheduled-message/{id}/cancel` | Cancelar | [↗](https://flwchat.readme.io/reference/post_v1-scheduled-message-id-cancel) |

**Modelos de Mensagem**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/template` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-template) |

**Sequências**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/chat/v1/sequence` | Listar | [↗](https://flwchat.readme.io/reference/get_v1-sequence) |
| `DELETE` | `/chat/v1/sequence/{id}/contact` | Remover contato | [↗](https://flwchat.readme.io/reference/delete_v1-sequence-id-contact) |
| `POST` | `/chat/v1/sequence/{id}/contact` | Adicionar contato | [↗](https://flwchat.readme.io/reference/post_v1-sequence-id-contact) |
| `DELETE` | `/chat/v1/sequence/{id}/contact/batch` | Remover contatos | [↗](https://flwchat.readme.io/reference/delete_v1-sequence-id-contact-batch) |
| `POST` | `/chat/v1/sequence/{id}/contact/batch` | Adicionar contatos | [↗](https://flwchat.readme.io/reference/post_v1-sequence-id-contact-batch) |
| `GET` | `/chat/v2/sequence/{id}/contact` | Listar contatos | [↗](https://flwchat.readme.io/reference/get_v2-sequence-id-contact) |


### CRM — `https://api.wts.chat/crm`

**Cards**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/crm/v1/panel/card/{cardId}/note` | Listar anotações | [↗](https://flwchat.readme.io/reference/get_v1-panel-card-cardid-note) |
| `POST` | `/crm/v1/panel/card/{cardId}/note` | Adicionar anotação | [↗](https://flwchat.readme.io/reference/post_v1-panel-card-cardid-note) |
| `DELETE` | `/crm/v1/panel/card/{cardId}/note/{noteId}` | Remover anotação | [↗](https://flwchat.readme.io/reference/delete_v1-panel-card-cardid-note-noteid) |
| `GET` | `/crm/v2/panel/card` | Listar | [↗](https://flwchat.readme.io/reference/get_v2-panel-card) |
| `POST` | `/crm/v2/panel/card` | Criar | [↗](https://flwchat.readme.io/reference/post_v2-panel-card) |
| `GET` | `/crm/v2/panel/card/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v2-panel-card-id) |
| `POST` | `/crm/v2/panel/card/{id}/duplicate` | Duplicar | [↗](https://flwchat.readme.io/reference/post_v2-panel-card-id-duplicate) |
| `PUT` | `/crm/v3/panel/card/{id}` | Atualizar | [↗](https://flwchat.readme.io/reference/put_v3-panel-card-id) |

**Painéis**

| Método | Path | O que faz | Doc |
|---|---|---|---|
| `GET` | `/crm/v1/panel/{id}` | Obter por ID | [↗](https://flwchat.readme.io/reference/get_v1-panel-id) |
| `GET` | `/crm/v1/panel/{id}/custom-fields` | Campos personalizados | [↗](https://flwchat.readme.io/reference/get_v1-panel-id-custom-fields) |
| `GET` | `/crm/v1/panel/{id}/lost-reason` | Listar motivos de perda | [↗](https://flwchat.readme.io/reference/get_v1-panel-id-lost-reason) |
| `GET` | `/crm/v2/panel` | Listar painéis | [↗](https://flwchat.readme.io/reference/get_v2-panel) |

<!-- ENDPOINTS:END -->
