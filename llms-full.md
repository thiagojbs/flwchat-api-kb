# flw.chat API — pacote completo

Gerado de https://flwchat.readme.io. Contém: referência rápida, guias oficiais e referência de todos os endpoints.

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


---

# Guias

# Autenticação

Entenda como autenticar suas requisições para utilizar a API.

Para uso da API deverá ser gerado um token permanente através da plataforma web.

O token pode ser gerado acessando a página de integrações `Ajustes > Integrações > Integração via API`).

Após gerar o token, informe-o nos `Headers` de cada requisição, utilizando a chave `Authorization` e o schema `Bearer`.

Exemplo: `Authorization: Bearer pn_0000000000000000000000`.

***

Você também pode realizar requisições diretamente a partir desta documentação. Para isso, bastar informar o token no campo adequado, assim como no exemplo abaixo:


---

# Paginação

Entenda como a paginação nos endpoints de listagem funciona.

### Requisição

Vários endpoints de listagem de entidades possuem paginação, que é controlada através dos seguintes atributos `pageNumber` e `pageSize`, enviados no corpo da requisição.

```json
{
  "pageNumber": 1,
  "pageSize": 50,
  ...
}
```

Sendo:

* `pageNumber`: indica qual página deseja obter;
* `pageSize`: indica o tamanho desta página, ou seja, quantos itens serão retornados, sendo possível no máximo 100.

Observe que ao alterar o `pageSize` em requisições subsequentes, o `pageNumber` retornará resultados diferentes. Portanto, é importante manter um `pageSize` constante enquanto se itera sobre o `pageNumber`.

***

### Resposta

Os resultados retornados nos endpoints paginados possuem a seguinte estrutura:

```json
{
  "pageNumber": 1,
  "pageSize": 50,
  "totalPages": 5,
  "totalItems": 250,
  "hasMorePages": true,
  "items:" [{...}],
  ...
}
```

Sendo:

* `pageNumber`: indica qual página foi obtida;
* `pageSize`: indica o tamanho da página obtida;
* `totalPages`: total de páginas existentes para a consulta atual;
* `totalItems`: total de itens existentes para a consulta atual;
* `hasMorePages`: indica se há mais páginas a serem consultadas, ou seja, se `pageNumber` é menor que `totalPages`;
* `items`: array de entidades retornadas, cujo tamanho será menor ou igual a `pageSize`.


---

# Rate limiting

Para garantir a estabilidade, segurança e desempenho da API, aplicamos limites de requisições. Eles funcionam em duas camadas complementares:

1. **Limite principal (uso contínuo)**\
   Você pode realizar até **`1.000` requisições a cada `5` minutos**, o que equivale a uma média aproximada de `3` requisições por segundo.\
   Esse limite controla o uso regular da API ao longo do tempo.

2. **Limite de proteção contra picos (burst limit)**\
   Além do limite principal, existe um limite adicional de segurança: **`200` requisições a cada `5` segundos.**\
   Esse mecanismo evita picos repentinos de chamadas que poderiam impactar a saúde e a estabilidade da aplicação, mesmo que o limite principal ainda não tenha sido atingido.

**Comportamento em caso de excesso**

Requisições que ultrapassarem qualquer um desses limites receberão como resposta o status `429 – Too Many Requests`, você deve esperar para que o limite seja reestabelecido para voltar a disparar mensagem.

> 📘 Escopo
>
> Os limites citados acima são aplicados por conta

<br />

## Dicas para evitar atingir o limite

Algumas boas práticas ajudam a manter sua integração estável e evitam respostas `429 – Too Many Requests`.

* **Evite loops sem controle**\
  Laços que disparam requisições em sequência (especialmente for ou while) devem sempre ter algum tipo de atraso ou controle de volume.
* **Implemente retry com espera (backoff)**\
  Se receber um 429, aguarde alguns segundos antes de tentar novamente. Repetir imediatamente tende a piorar o problema.
* **Distribua as chamadas ao longo do tempo**\
  Em vez de disparar muitas requisições de uma vez, espalhe-as de forma uniforme para manter uma média estável.

## Dicas específicas para quem usa n8n\*\*

O n8n é poderoso, mas pode gerar picos de requisições sem perceber. Algumas configurações ajudam bastante:

* **Use o node Wait**\
  Após chamadas em massa ou dentro de loops, utilize o node Wait para inserir um atraso entre as execuções.\
  Mesmo um intervalo pequeno (ex: 500 ms) já reduz drasticamente o risco de atingir o limite.
* **Controle a concorrência**\
  Ao usar nodes como HTTP Request e Split In Batches, evite executar muitos itens em paralelo. Prefira processar em lotes menores e sequenciais.
* **Configure corretamente o Split In Batches**\
  Use tamanhos de lote menores (ex: 10 ou 20 itens).\
  Combine com o node Wait entre os lotes para suavizar o volume de chamadas.
* **Trate o erro 429 explicitamente**\
  Configure o fluxo para:\
  -Detectar o erro 429\
  -Aguardar alguns segundos\
  -Repetir a requisição automaticamente\
  -Isso evita falhas no workflow e respeita os limites da API.


---

# Login integrado

É possível integrar o login entre plataformas, gerando um token via API e direcionando o usuário

Para integrar o login, você precisará de um **token permanente**, que pode ser obtido em Ajustes → Integração → Integração via API.

Com esse token, sua aplicação backend faz uma requisição POST para autenticar um usuário, definindo em qual conta ele será logado e para qual página será redirecionado.

***

## Parâmetros da Requisição

### Identificação do usuário

| Parâmetro     | Descrição                                                                                                                                    |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `phoneNumber` | Número de telefone do usuário. Para números nacionais, não é necessário formatação especial. Para internacionais, inclua o `+` antes do DDI. |
| `email`       | E-mail cadastrado na plataforma.                                                                                                             |
| `redirectUrl` | URL da página que o usuário acessará após autenticado. Ideal para direcionar diretamente a uma conversa específica. *(opcional)*             |

***

## Componente de Conversas

O componente de conversas está disponível na rota `/chat2/sessions/XXXXXX`, onde `XXXXXX` é o ID da conversa. Há duas variações úteis:

* **`/preview`** — Suprime o menu da plataforma, exibindo apenas a conversa.
* **`?interactive=true`** — Pré-habilita a interação na conversa.

Combinando os dois, a URL completa fica:

```
/chat2/sessions/XXXXXX/preview?interactive=true
```

***

## Fazendo a Requisição

> 🚧 **Atenção:** nunca faça essa requisição no front-end. Ela deve ser realizada exclusivamente via **backend** para preservar a segurança dos seus dados.

Passe o token permanente no cabeçalho usando autenticação **Bearer**:

```
Authorization: Bearer pn_000x000x000x000x000x000x000x00
```

**POST** `https://api.flw.chat/auth/v1/login/authenticate`

**Requisição**

```json
{
  "phoneNumber": "5531999999999",
  "email": "email@seudominio.com",
  "redirectUrl": "/chat2/sessions/df98b9fb-2280-45z5-bce1-3fe8aa7047e5/preview"
}
```

**Resposta**

```json
{
  "userId": "48525e80-43a7-4e06-86e0-f6b67b7d6629",
  "tenantId": "d4ed253d-f0c6-435c-8f7f-59a0598885fe",
  "urlRedirect": "https://xyz.flw.chat/auth/external-login?code=3aXTxVyWtU5p6x7PpGmtlL62XRjbmKUFIWxADykpaWQ&userId=58525e80-43z7-4e06-86e0-f6b67b7d6629&tenantId=d4ed253d-y0c6-435c-8f7f-59a0598885fe",
  "expiresIn": "2026-01-01T00:00:00Z"
}
```

Após receber a resposta, utilize o campo `urlRedirect` para redirecionar o usuário, ele iniciará a sessão já autenticado.


---

# Webhooks

Entenda como receber eventos em outro sistema.

O envio de eventos por webhook é um mecanismo para notificar o seu sistema quando uma variedade de interações ou eventos acontecem, incluindo quando uma pessoa envia uma mensagem ou um contato é alterado.

***

### Configuração

É possível realizar a configuração através da plataforma (acessando `Ajustes > Integrações > Webhooks` ).

Ao criar uma nova assinatura, você deverá selecionar os eventos/tópicos que deseja assinar e informar uma URL válida. A plataforma enviará requisições HTTP utilizando o método `POST`  para a URL informada, que deverá estar preparada e disponível publicamente para receber os eventos.

É possível pausar temporariamente o recebimento de webhooks, modificando os status da assinatura para inativo.

### Ciclo de vida de uma conversa

![](https://files.readme.io/7a99955-Captura_de_Tela_2023-10-25_as_18.39.39.png)

***

### Estrutura

As mensagens de webhook enviadas possuirão o corpo no formato `application/json` e a seguinte estrutura:

```json
{
    "eventType": "NOME_DO_EVENTO",
    "date": "DATA_DE_ENVIO",
    "content": { ... }
}
```

Sendo:

* `eventType`: o nome do evento/tópico, sendo os valores possíveis listados [abaixo](#eventos);
* `date`: data e hora de geração do evento, seguindo o formato `YYYY-MM-DDTHH:mm:ss`;
* `content`: conteúdo do evento.

Veja abaixo um exemplo de webhook de alteração de contato:

```json
{
    "eventType": "CONTACT_UPDATE",
    "date": "2023-08-23T16:42:35.4359934Z",
    "content": {
        "id": "ed2b52f8-cf13-449b-b3d5-ae27051f4663",
        "createdAt": "2022-10-28T21:24:26.158391Z",
        "updatedAt": "2023-08-23T16:15:35.3814324Z",
        "companyId": "626fb5de-0cc2-4209-b456-47b454ee6e14",
        "name": "John Raymond Legrasse",
        "phonenumber": "+55|00000000000",
        "phonenumberFormatted": "(00) 00000-0000",
        "email": "exemplo@email.com",
        "instagram": null,
        "annotation": "",
        "tagsId": [],
        "tags": [],
        "status": "ACTIVE",
        "origin": "CREATED_FROM_HUB",
        "utm": null,
        "customFieldValues": {},
        "metadata": null
    }
}
```


---

# Webhook no Chatbot

Durante o atendimento pelo Chatbot, o sistema poderá disparar webhooks para buscar mais informações, dados e criar fluxos alternativos para uma melhor experiência dos clientes.

![](https://files.readme.io/ef08e9d-Captura_de_Tela_2024-01-23_as_14.57.27.png)

O webhook no chatbot tem uma mensagens de input e output padrões, você define a URL e recebe a mensagem via método `POST`.

**Mensagem de disparo:**\
Esta mensagem será enviada pelo chatbot para seu sistema com todos os dados capturados até o momento, os dados do canal de atendimento, dados do contato e as opções de respostas possíveis:

```json JSON
{
    "responseKeys": [
        "CLIENTE_EXISTE",
        "CLIENTE_NAO_EXISTE"
    ],
    "sessionId": "567ca9b8-eaa9-4a33-8cf9-d2c67060af74",
    "session": {
      "id": "567ca9b8-eaa9-4a33-8cf9-d2c67060af74",
      "createdAt": "2024-06-02T12:00:10.38771Z",
      "departmentId": "07deebd3-dede-42d1-9169-75e00efdf088",
      "userId": null,
      "number": "2024062700164",
      "utm": {
        "clid": "asldkjasLKJASLKDJLKJASLDKJASGFui3HT7c7KUdBaB7lOHHxp5CxufCY0GjlvZcDRpsTaRbZMQ",
        "term": null,
        "medium": "REFERRAL",
        "source": "INSTAGRAM",
        "content": "Campanha de Natal Minas Gerais!",
        "campaign": "776107696326",
        "headline": "Converse conosco",
        "referralUrl": "https://www.instagram.com/p/x466u6s5ykjs/"
      }
    },
    "channel": {
        "id": "0a4ca3cd-b9fd-4523-a032-5a343bf7b209",
        "key": "551140037752",
        "platform": "WhatsApp",
        "displayName": "(11) 3000-0000"
    },
    "contact": {
        "id": "f8f43b22-2f20-42f3-be13-65bf90282143",
        "name": "David",
        "phonenumber": "+55|1199999999",
        "display-phonenumber": "(11) 99999-9999",
        "email": "email@gmail.com",
        "instagram": null,
        "tags": [
            "Lead"
        ],
        "cnpj": "00.000.000/0000-00",
        "metadata": { "cod-ext": "abcd" }
    },
    "questions": {
        "cb-ec36e3fe-qst-c0b0875a": {
            "text": "Qual seu CNPJ?",
            "answer": "00.000.000/0000-00"
        }
    },
    "menus": {
        "cb-ec36e3fe-mn-943b055a": {
            "text": "Qual opção você deseja?",
            "answer": "Comprar"
        }
    },
    "lastMessage": {
      "id": "152d4d13-0b13-49bb-bafc-3923434f204b",
      "createdAt": "2024-06-27T19:09:22.592061Z",
      "type": "IMAGE",
      "text": null,
      "fileId": "aa546fa6-ca68-4a8b-a57d-c031460fae69",
      "file": {
        "publicUrl": "https://cdn.flw.chat/upload/88fb5de-0cc2-4209-b456-47b454ee6e14/IMAGE/c40e85e_20240627190923197_436019626068697.jpg?AWSAccessKeyId=XXXX",
        "extension": ".jpg",
        "mimeType": "image/jpeg",
        "name": "436019626068697.jpg",
        "size": 233541
      }
    }
}
```

**Mensagem de retorno (Simples)**\
Seu webhook deverá responder com um código HTTP `200` para seguir no fluxo principal de sucesso, mas você poderá criar fluxos alternativos, assim deverá responder com o código HTTP `200` e uma mensagem conforme abaixo:

```json
{
    "response": "CLIENTE_EXISTE"
}
```

**Mensagem de retorno (Com dados do contato)**\
Você poderá atualizar os dados do contato no retorno do webhook, bem como metadados para serem usados em outro momento de integração, como no exemplo abaixo o código do cliente no seu sistema.

```json
{
    "response": "CLIENTE_EXISTE",
    "metadata": {
        "cliente-existe": true
    },
    "contact": {
        "cnpj": "00.000.000/0000-00",
        "metadata": {
            "cod-ext": "abcd"
        }
    }
}
```

**Mensagem de retorno (Com disparo de mensagens)**\
Também é possível enviar mensagens ao usuário ao retornar do webhook, você deverá indicar uma lista de mensagens que serão disparadas na ordem enviada;

```json
{
    "response": "CLIENTE_EXISTE",
    "messages": [
        {
            "text": "Segue seu boleto abaixo para pagamento. Vencimento dia 10/01"
        },
        {
            "fileUrl": "https://xyz.com/boleto.pdf"
        },
        {
            "template": {
                "id": "ab78cd_oferta",
                "parameters": {
                    "valor": "R$ 9,99"
                }
            }
        }
    ]
}
```

As mensagens podem incluir texto e/ou arquivo. Além disso, é possível utilizar um modelo de mensagem (template) previamente criado.

As opções de respostas foram separadas para efeitos didáticos, mas podem ser combinadas em uma única mensagem.

***

## Perguntas Dinâmicas

Este recurso permite carregar opções de resposta em tempo real diretamente do seu sistema via Webhook. No momento em que o cliente atinge a etapa correspondente no fluxo, o chatbot realiza a requisição e renderiza as alternativas retornadas.

**Parâmetros do Objeto de Resposta**

| Parâmetro | Tipo   | Obrigatório | Descrição                                                                                                  |
| --------- | ------ | ----------- | ---------------------------------------------------------------------------------------------------------- |
| `text`    | String | Opcional    | Texto principal da pergunta. Pode ser omitido se a opção "Definir como mensagem fixa" estiver ativa no nó. |
| `type`    | String | **Sim**     | Define o formato de exibição. Valores aceitos: `BUTTONS`, `LIST` ou `NUMBERS`.                             |
| `options` | Array  | **Sim**     | Lista de objetos contendo as opções para seleção (máximo de 50 itens).                                     |

**Estrutura do Array `options`**

Cada objeto dentro da lista de opções suporta os seguintes campos:

* `text` **(Obrigatório)**: O rótulo ou texto principal da opção exibida ao usuário.
* `description` **(Opcional)**: Subtítulo ou descrição de apoio. Disponível exclusivamente para o tipo `LIST`.
* `url` **(Opcional)**: Link para redirecionamento externo. Disponível exclusivamente para o tipo `BUTTONS`.

**Exemplo de Retorno JSON**

```json
{
  "text": "Como podemos ajudar hoje?",
  "type": "BUTTONS",
  "options": [
    {
      "text": "Área de Cliente",
      "url": "https://empresa.com/cliente"
    },
    {
      "text": "Suporte Técnico"
    }
  ]
}
```


---

# Rastreio de campanha UTM

Entenda como rastrear sua campanha utilizando padrões UTM

Os padrões UTM são parâmetros adicionados às URLs para ajudar a rastrear a eficácia das campanhas, esses padrões permitem que você identifique de onde os visitantes estão vindo e quais campanhas são mais eficazes.

***

Um exemplo de uma URL com parâmetro UTM

`https://api.flw.chat/chat/v1/channel/wa/[TELEFONE]?text=[MENSAGEM]&utm_source=[SOURCE]&utm_medium=[MEDIUM]&utm_campaign=[CAMPAIGN]`

**Parâmetros**

**\[TELFONE]**: Inserir telefone da sua empresa no formato "5511980009999";\
**\[MENSAGEM]**: Inserir a mensagem que será enviada pelo cliente no WhatsApp. Ex.: Quero saber mais;\
**\[MEDIUM]**: Meio onde vai ser difundida a campanha independentemente da fonte. Ex.: Stories;\
**\[SOURCE]**: Plataforma de origem do lead. Ex.: tiktok;\
**\[CAMPAIGN]** : identifica a campanha. Ex.: PublicoAberto;

***

Assim que a conversa for iniciada, você verá a mensagem abaixo podendo ver a origem do lead.

![](https://files.readme.io/af1af8dd77ea112d7eae8958c87ac01390becb36419f221d0837dcd4a25dc60f-image.png)

Além deste ponto você conseguirá ver na origem do contato e no relatório de indicadores e de atendimentos.

<br />

<br />

![](https://files.readme.io/7eb194fc3093006500316a099c3b5791324ea982f1dce00ef30ea9c69c0d03de-image.png)


---

# Informações para Firewall

Empresas que tem regras mais rígidas de firewall podem usar as informações abaixo para configurar suas regras

**Acesso web**\
`https://*.flw.chat` e  `https://*.wts.chat`

**API**\
`https://api.flw.chat` e  `https://api.wts.chat`

**Download de arquivos**\
`https://cdn.flw.chat` e  `https://cdn.wts.chat`

**Upload de arquivos**\
`https://wts-storage.s3.sa-east-1.amazonaws.com`

**Conexão websocket web**\
`wss://rt-web.flw.chat` e `wss://rt-web.wts.chat`

**Conexão websocket app mobile**\
`wss://rt.flw.chat` e  `wss://rt.wts.chat`

**IP de chamadas de webhook**\
`18.215.79.89`

**Distribuição de conteúdo / arquivos**\
`https://ip-ranges.amazonaws.com/ip-ranges.json`\
*Utilizamos o serviço `CLOUDFRONT `da AWS para fazer a distribuição de arquivos, para liberação no firewall é necessário adicionar os ranges de ips da AWS*


---

# 1. Criar um assistente

Neste primeiro passo vamos criar juntos um agente IA e configurar as primeiras etapas da integração com o assistente no N8N.

Antes de tudo vamos criar nosso assistente IA, configurar o modelo e criar uma chave de API.

## Como criar uma conta na OpenAI

* Acesse o site da OpenAI (<https://platform.openai.com>) no seu navegador.
* Inicie o cadastro: clique no botão "Sign Up" ou "Registrar-se" no canto superior direito da página.
* Preencha suas informações: insira seu endereço de e-mail ou, se preferir, faça login diretamente com uma conta Google ou Microsoft. Em seguida crie uma senha.
* Verificação de e-mail: após fornecer suas informações e criar uma conta, você receberá um e-mail de verificação. Acesse sua caixa de entrada e clique no link de verificação enviado pela OpenAI.
* Preencha seus dados pessoais: pode ser solicitado o fornecimento de informações como seu nome e telefone para verificação.
* Escolha um plano: a OpenAI oferece tanto uma versão gratuita quanto planos pagos com mais recursos. Escolha o que melhor se adequa às suas necessidades.

***

## Como criar um projeto dentro da OpenAI

* Após criar sua conta na OpenAI, será possível acessar o painel onde você poderá criar o seu assistente.
* No painel, clique em "Dashboard".
* Depois, clique em "Assistants".

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1884fc9cfbadab6cbe9b395cce670fc856b0a0cb618daf59c8470345b496481a-WTS.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Clique em "Create".
* Ao clicar em "Create", será aberta a tela acima onde você poderá dar um nome ao seu assistente no campo "Name".
* No campo "System instruction", você deverá definir como o assistente deve se comportar. Exemplo:

> **Você deve se comportar como um corretor de imóveis. Pergunte ao cliente sobre o tipo de imóvel, localização desejada, número de quartos, banheiros, vagas de garagem e faixa de preço. Responda perguntas frequentes de forma rápida e objetiva. Transfira para o atendimento humano se a informação disponível não for suficiente.**

* Defina o modelo no campo "Model" — recomendamos o gpt-4o-mini por ser um modelo completo e mais rápido que outros.
* Em seguida, é possível definir configurações adicionais como "File search" que permite que o assistente tenha conhecimento dos arquivos que você ou seus usuários carregam. Depois que um arquivo é carregado, o assistente decide automaticamente quando recuperar o conteúdo com base nas solicitações do usuário e, também, o "Code Interpreter" que permite que o assistente escreva e execute códigos.
* Configure o "Response Format" para "Text".
* Deixe os campos "Temperature" e "Top P" default, no futuro ajuste para que a resposta seja mais adequada ao tom que você deseja que o assistente responda.

***

## Como criar uma chave de API

* No menu lateral, clique em "API Keys".
* Na página de "API Keys", clique no botão "Create new secret key", como demonstra a imagem abaixo:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/43e2c8e270320cec6ab59a1a01942b68fcdcc679b147031f5542879e44a572a1-WTS_3.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Um pop-up aparecerá mostrando sua nova chave de API. **Copie a chave imediatamente**, pois você não poderá visualizá-la novamente.
* Essa chave será usada para autenticar suas solicitações ao utilizar a API da OpenAI.
* Se precisar, você pode revogar ou criar novas chaves a partir dessa mesma tela a qualquer momento.

<br />

**Lembre-se de que a chave de API é privada e você não deve compartilhá-la publicamente, pois ela dá acesso à sua conta e aos seus créditos da OpenAI.**


---

# 2. Criar o loop no chatbot

Entenda como criar o modelo de chatbot e configurar o loop de modo que as mensagens enviadas não se percam e sejam sempre processadas por seu assistente.

## Como criar o modelo do chatbot

* Dentro da plataforma faça login com o usuário administrador e siga os passos abaixo para criar o modelo do chatbot que será integrado à IA.

* No menu de opções clique em **Apps** > **Chatbot** > **Novo**.

* Dê um nome ao seu chatbot e o associe a um tipo de canal (Z-API ou WhatsApp oficial). Defina a equipe padrão desse chatbot.

* Crie um nó de mensagem receptiva. Exemplo: *Olá, boas-vindas! Como posso ajudar?*

* Em seguida, configure uma ação que aguarde resposta do contato com as opções: **"Limite de espera: Sem limite"** e **"Tolerância: 5 segundos"**.

* Acima do nó de "Aguardar resposta do contato" é necessário criar um ponto de retorno. Atenção: sem este ponto de retorno o loop não irá funcionar.

* Em seguida, é preciso configurar o disparo webhook que enviará as informações do atendimento.

* No campo **URL** copie a URL do webhook que deverá ser criado no N8N e cole no campo "URL". Clique em **"Atualizar"** para salvar as configurações.

[block:image]{"images":[{"image":["https://files.readme.io/2a68c3db185774771513e3170f7bd6d9f9b88f50a23c066ababadae59bf9f9be-image.png",null,null],"align":"center","border":true}]}[/block]

<br />

***

## Como criar os loops

* Dentro do subfluxo de **"Sucesso"** crie uma ação que redireciona para o ponto de retorno **"GPT"**, como mostra a imagem acima.
* Assim, o loop estará configurado de modo que sempre que o contato enviar uma mensagem a mesma voltará ao ponto de retorno configurado e será disparada via webhook criando o loop.

  ![](https://files.readme.io/1cea14fb4be34843910e0885f9dfb82d2376afb50718f3e6d2f53f1fca4baec3-image.png)

<br />

* No subfluxo de **"Falha no envio"** adicione uma mensagem de modo que o contato seja informado que a mensagem dele falhou ou não foi compreendida, logo após adicione outro ponto de retorno **"GPT"**, assim como no fluxo de "Sucesso no envio"

  ![](https://files.readme.io/cda5cd9b183db87645645cf2aaf482e281d973361e593fe392f47b757f0c4dba-image.png)

<br />

Após seguir os passos acima, salve seu chatbot, publique e o associe ao canal em que os clientes entrarão em contato e serão respondidos por seu assistente.


---

# 3. Como ler e responder textos

Vamos adicionar a capacidade de ler e responder textos usando o ChatGPT.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

![](https://files.readme.io/cfefb1c37cf1a3dfbb0565c56dc4962574eda264966f4ad202eac5961ce13215-image.png)

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_response_with_text.json) .
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

***

# Como fazer

## Montando o escopo da integração

* Crie uma conta no [N8N](https://n8n.io/).
* Clique em "Add workflow".
* Em seguida, clique em "Add first step".
* Selecione o node "On webhook call".
* Altere o método "HTTP" para **"Post"**.

***

## Armazenando variáveis

* Crie um node "Edit Fields".
* Crie uma variável chamada text e armazene nessa variável o valor "lastMessagesAggregated". Veja imagem abaixo

  ![](https://files.readme.io/facbcd30f03b11a64240d77c4287b5960eef156874099cfd664fd92db60b382c-image.png)

***

## Configurando o node do assistente

* Logo após criar o webhook, é preciso criar o node do assistente IA.
* Para isso, clique em "+" digite **"OpenIA"** e selecione **"Message an assistant"**.
* Adicione a credencial que foi criada dentro da plataforma da OpenIA, essa credencial será a chave da API que você criou no passo 3 da etapa [Criar um assistente](https://flwchat.readme.io/reference/1-criar-um-assistente-1).
* Nas opções "Resource" e "Operation" deixe ambos default.
* Em "Assistant" selecione o assistente que você criou na etapa [Criar um assistente](https://flwchat.readme.io/reference/1-criar-um-assistente-1).
* Em "Prompt" selecione a opção "Define below", no campo "text" passe a variável "text" que gravamos no node anterior "Edit Fields".

  ![](https://files.readme.io/ae767047c740f4d42a51d78e0c20c5976fda75c90c94fbaf99089f7d85fd935a-image.png)

<br />

* Em "Memory" defina para "Use memory connector". Será criado um nó abaixo do nome "Window Buffer Memory", nele é preciso passar o ID da sessão (presente no webhook).

> ### Atenção
>
> Definir a memória é muito importante, ela que fará com que o assistente consiga entender o contexto da conversa.
>
> ![](https://files.readme.io/5df3223a5bdecaf177473b259690b565fe6dc883ef21de2574e6a168eab20746-image.png)
>
> <br />

***

## Ferramentas do assistente IA

O assistente assistente possui ferramentas (Tools), que permite interações com outros sistemas através de requisições HTTP, isso torna-se útil e abre um leque de opções, você pode fazer requisições para buscar um boleto em um banco de dados e retorna-lo para o contato por exemplo, nesse documento vamos abordar três funcionalidades, mas o céu é o limite tratando-se dessa funcionalidade.

1. Nessa primeira etapa vamos realizar uma requisição na API para buscar as equipes de uma conta, essa lista de equipes dará uma base ao seu agente para transferir o contato de acordo com o contexto da conversa.

* Clique em tools e crie uma requisição HTTP
* Em "Description" você deve dar instruções para o agente da função, segue uma sugestão: "Nesta função você consegue listar as equipes disponíveis para transferência".
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/get_v2-department).
* Ao configurar o header defina o "Value Provided" como "Using Field Below". Veja imagem abaixo

  ![](https://files.readme.io/358fe8a6d87ef75b4e5762813d0508afdc2507743637092ef2839bfef9ba105c-image.png)

2. Nessa etapa vamos configurar a função de transferência de equipe, também vamos criar uma requisição HTTP, para o endpoint de transferir conversas.

* Assim como na etapa anterior vamos dar algumas instruções para nosso assistente IA sobre como usar essa função, segue uma sugestão:\
  **Setores para transferência.**\
  **Algumas diretrizes:**\
  **-Seja rápido e objetivo ao responder perguntas frequentes, buscando entender detalhadamente o problema do contato.**\
  **-Explique de maneira simples qualquer processo técnico de baixa complexidade.**\
  **-Demonstre paciência ao lidar com questões delicadas ou frustrações dos clientes.**\
  **-Utilize um tom positivo e otimista, mesmo ao comunicar informações difíceis ou negativas**.\
  **-Não solicite dados do contato como (e-mail, Id, números de protocolo, documentos).**
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/put_v1-session-id-transfer).
* Marque a opção "Send Body" e cole o JSON abaixo no body da requisição.

```json
{
  "type": "DEPARTMENT",
  "newDepartmentId": "{departmentId}"
}
```

* Você deve usar um placeholder para quaisquer dados a serem preenchidos pelo modelo. Veja imagem abaixo

  ![](https://files.readme.io/9c47ae4c1fa9260cab44ea338517f64f7233a6916b49c2e8742882392c1c6fc9-image.png)

3. Por fim, a função de concluir atendimento, nessa etapa vamos configurar uma outra requisição para finalizar o atendimento quando solicitado pelo contato. Siga os passos abaixo

* No campo "Description" passe as instruções para seu assistente IA.
* Configure a requisição de acordo com a [documentação](https://flwchat.readme.io/reference/put_v1-session-id-complete).
* Marque a opção "Send Body" e cole o JSON abaixo no body da requisição
* ```json
  {
    "reactivateOnNewMessage": true
  }
  ```

  ![](https://files.readme.io/e395c0cd565d4c4ffa909f2c9c435968e37b079209006e47990240b1b7554735-image.png)

  ***

  ## Configuração do node de enviar mensagem ao contato
* O primeiro passo é instalar o módulo do WTS em seu N8N. É possível encontrar essa informação para a instalação em "Ajustes" > "Integrações" > "Automações via N8N".
* Após instalar o módulo WTS, crie uma chave de API dentro da plataforma em "Ajustes" > "Integrações" > "Integrações Via API" > "Novo" > "Nomeie a chave" > "Salve" > "Copie".
* Clique para adicionar um novo nó e digite "WTS", procure por "Session Actions" > "Send Message Text".
* Em "Credential to connection with", caso você já tenha uma chave de API criada, bastar selecioná-la. Caso não, basta criar uma nova "Create new credential" e colar a chave API criada na plataforma.
* O output em questão é a resposta do seu agente, você deve passá-lo dentro da requisição para disparar essa resposta para o contato.
* No campo "Text" coloque o output retornado por seu agente IA, no campo "Session ID" informe o id da sessão (essa informação você encontra no output do webhook, procure por "sessionId").

  ![](https://files.readme.io/32bd80ce5b147a49d540fee71eb35c23da1f13b56c6bec8a36ad78882e24f370-image.png)

Seguindo esse tutorial, será possível ler e responder textos usando o ChatGPT, além disso será possível executar funções de transferência e conclusão de atendimentos. Você também pode adicionar outras funções ao seu assistente, como buscar boletos em uma API externa por exemplo, existem diversas possibilidades que você pode explorar utilizando as ferramentas do seu assistente.


---

# 4. Como processar áudios

Nessa etapa vamos ensinar como adicionar a capacidade de processar áudios à sua IA.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

![](https://files.readme.io/7cc1583c454c1a0441643149950d2cdafb2d08bef63adb07def0e4575c8bd7a6-image.png)

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_transcribe_audio.json).
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

## Separando os tipos de mensagem

Como explicado anteriormente, mensagens agregadas são divididas em mensagens de texto e mensagens que contenham áudio, imagem ou arquivo. Para separarmos as mensagens de texto das mensagens que contenham arquivos, vamos usar o node "Filter" validando se o tipo de mensagem "Text" é ou não vazio.

* Se não for vazio vamos usar um "Set" para gravar a várivel "lastMessagesAggregated.text" e, caso seja vazio, serão  enviadas apenas mensagens do tipo "File",  vamos tratar sobre mais a frente.

<br />

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/71fc809bc4c502da99eb9943f229c9850a781eb0b9c7ea44e93591ea0ab93402-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Já para mensagens "Files" devemos dividir os arquivos vindos do webhook em arquivos únicos, usando o node "Split Out" e tratar cada tipo de arquivo de uma maneira. Nessa etapa vamos tratar apenas arquivos de áudio, outros tipos de arquivos serão abordados mais a frente.

[block:image]{"images":[{"image":["https://files.readme.io/e7c75bd3c0081ce3d348d9c5298682a3b463db1d52f5da648eb28fb9e8841acc-image.png",null,""],"align":"center","border":true}]}[/block]

* Após dividirmos os arquivos vamos separá-los por tipo, áudio, imagem e documentos. Para isso usaremos o node "Switch" e comparar se o "file.mimeType" (tipo de arquivo) começa com áudio/(formato) do arquivo.

[block:image]{"images":[{"image":["https://files.readme.io/7af17401bbc21aa3d7560ece8c31595cc9099638341708ad4427a6c4aae10cf8-image.png",null,""],"align":"center","border":true}]}[/block]

***

## Tratando arquivo de áudio

* Após separar o arquivo de áudio dos demais, é preciso fazer o seu download. Para isso usaremos uma requisição HTTP, vamos dar um "GET" na URL pública que se encontra o áudio.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c479446f08f8c7de2912467eeb97adc6c1449024ae15df08aa5bb7c56f312686-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

***

## Transcrevendo o áudio

* Logo após realizar o download do áudio, crie um node OpenIA > "Transcribe Recording".

* No campo "Input Data Field Name" é necessário passar o nome do campo de entrada que contém os dados do arquivo binário a serem processados.

[block:image]{"images":[{"image":["https://files.readme.io/204196db3bcddd8f53201fd10a3890f6707cd323a80b3f59108dfb06ba9072d2-image.png",null,""],"align":"center","border":true}]}[/block]

* Grave o output da transcrição em uma variável.
* Crie um node "Merge" para agrupar os inputs.
* Grave os valores "text" e "sessionId" em um node "Set".

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/564f668d83d296a519040ff68fc620715a5ede2a0f10014fe43997892da0fcc4-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

* Em seguida, é necessário concatenar as mensagens em uma única mensagem para enviarmos para o seu assistente.  Para isso será utilizado um node "Code", basta copiar o código abaixo:

```javascript
var text = "";
var sessionId = $('Webhook').first().json.body.sessionId;

for (const item of $input.all()) {
  text += item.json.text + " \n";
}

return { "text": text, "sessionId": sessionId };
```

***

### Resumo do que o código faz:

1. Inicializa uma variável text como uma string vazia.
2. Recupera o valor do sessionId de uma resposta de webhook anterior.
3. Itera por todos os itens de entrada disponíveis e concatena o texto de cada item, adicionando uma nova linha entre os textos.
4. Retorna um objeto com o texto concatenado e o sessionId para ser usado em outro lugar.

* Ligue o node "Code" ao seu assistente, que por sua vez estará ligado ao node "Enviar mensagem".

Após todos esses passos sua integração irá processar áudios enviados, transcrevendo-os em texto para que seu assistente consiga interpretar e responder da forma mais adequada.


---

# 5. Como processar imagens

Nessa etapa vamos ensinar como adicionar a capacidade de processar imagens à sua IA.

**Confira abaixo como ficará a integração após seguir esse tutorial.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/369776debe631f1056604367ea9f710eab5f720f7ebd09ee18394d33c8e89ec7-image.png",
        null,
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

> 📘 Para baixar o fluxo pronto, o JSON com todos os passos está [nesse link](https://github.com/wtschat/files/blob/main/wts_n8n_transcribe_image.json).
>
> Você poderá criar seu próprio fluxo, para facilitar você pode baixar o nosso fluxo e alterar.

## Processando imagens

* Na etapa anterior no processamento de áudio foi criado o node "Switch" para processar diferentes tipos de arquivo, vamos criar uma rota dentro desse switch para processar as **imagens.**

* Para isso, é necessário comparar se o "file.mimeType" (tipo de arquivo) começa com image/ + (formato) do arquivo, assim como foi feito para o áudio. Confira a imagem abaixo:

[block:image]{"images":[{"image":["https://files.readme.io/6291b8bb5c1840b9ee157b48677d63afdf81b190962700520d60f28f33defc68-image.png",null,""],"align":"center","border":true}]}[/block]

* Grave o "Content" (resultado da transcrição da imagem) em uma variável

  ![](https://files.readme.io/580a4203a135f4df22c16ef8e685b2a13ca6f231a89652a3dbdd68a05cd74861-image.png)
* Após esses passos basta ligar o node "Set" (que contém a variável da transcrição da imagem) ao "Merge". Como mostra a imagem inicial desse documento
* Salve seu workflow.

<br />

Seguindo esse rápido tutorial será possível processar imagens com IA.


---

# Criar token para integração

Um token permanente permite que você autentique e autorize seu aplicativo sem ter que implementar fluxos de autenticação. Basta criar um novo token e usá-lo para autenticação onde quiser.

Para criar um token de autenticação clique em **Ajustes > Integrações > Integração via API (Configurar)**. Em seguida, clique em **Novo** e adicione um nome para o token.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/828e12c05b6f3fcf45df249ebad77a6391c8fc35c503fe25f7af7f54e28dcfde-Token.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]

### Uso do token em uma chamada Http

Para utilizar o token permanente, você deve incluí-lo no cabeçalho (header) da requisição HTTP. Use o formato abaixo para garantir o acesso:

**Header "Authorization":** Bearer {seu\_token\_aqui}

```curl
curl -X GET "https://api.flw.chat/v1/channel" \
     -H "Authorization: Bearer pn_TOKEN_PERMANENTE"
```

### Orientações de segurança

**Geração do Token:** Você pode gerar um novo token permanente sempre que precisar, informe o nome da plataforma que irá utilizar o token para que você consiga identificar no futuro. Esse token é uma chave única que permite acesso direto aos nossos serviços, sem necessidade de login contínuo.

**Uso do Token:** O token permanente pode ser utilizado em integrações externas e ferramentas que precisem acessar sua conta. Lembre-se de mantê-lo seguro, pois ele dá acesso direto à sua conta.

**Revogação do Token:** Você tem o controle total do token permanente. Caso não precise mais dele ou queira reforçar a segurança, você pode excluí-lo a qualquer momento. Uma vez excluído, todas as integrações que utilizavam esse token deixarão de funcionar.

**Segurança:** Recomendamos não compartilhar seu token com terceiros e, se suspeitar de algum uso indevido, exclua-o imediatamente e gere um novo.


---

# MAKE

O **Make.com** é uma plataforma de automação que permite criar fluxos de trabalho personalizados para integrar diferentes aplicativos e serviços, eliminando tarefas manuais e repetitivas. Com uma interface visual intuitiva, os usuários podem conectar ferramentas e configurar gatilhos e ações para automatizar processos.

### Como funciona a contagem:

* **Operação**: Cada vez que um módulo em um cenário é executado, ele conta como uma operação. Por exemplo:
  * Buscar dados em uma planilha: 1 operação.
  * Enviar uma mensagem via e-mail ou Slack: 1 operação.
  * Processar dados de várias linhas: cada linha pode contar como uma operação separada.
* **Cobrança**:
  * **Plano contratado**: Cada plano (Gratuito, Core, Pro, etc.) tem um limite de operações mensais.
    * **Exemplo**: Um plano Core pode oferecer 10.000 operações por mês.
  * **Excedente**: Se o limite for atingido, os cenários param de executar até que:
    * O limite seja renovado no próximo ciclo.
    * Você faça um upgrade para um plano superior.

### Autenticação - Make.com

Um token permanente permite que você autentique e autorize seu aplicativo sem ter que implementar fluxos de autenticação OAuth 2.0. Basta criar um novo token e usá-lo para autenticação onde quiser.

Tutorial de instalação do aplicativo wtschat no Make.com

Passos para instalação

1. ### Acesse o Link do Aplicativo Make

   Abra o navegador e acesse o [link ](https://www.make.com/en/hq/app-invitation/0e94c36cbd3949661d56ad6aa33a80df)específico do aplicativo Make. Clique no botão “Instalar” para iniciar o processo.

   ![](https://files.readme.io/dab813e8d75ffeaec47b23d825d9d2b37b833d63a144a6f471ee33e5f04f7e83-image.png)
2. ### Complete a Instalação do Aplicativo

Você será redirecionado para uma página onde deverá selecionar a organização na qual deseja instalar o aplicativo. Selecione a organização desejada e clique no botão “Instalar” localizado no canto inferior direito da tela.\
Observação: A instalação só pode ser feita em uma organização na qual você possui a função de “administrador” ou “desenvolvedor de aplicativos”.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ef661dee5d39df4742fde9a3c0c359d2a85f53ee3456126d3a8619ce3190f063-INSTALAO_1.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]

3. ### Confirmação de Instalação
   Uma notificação aparecerá na tela indicando que a instalação foi concluída com sucesso. Clique em "Finish Wizard"

<br />

4. ### Acesse o Make
   Abra o Make e acesse a organização onde você instalou o aplicativo. Navegue até “Aplicativos Instalados” para visualizar o ícone e o nome do aplicativo "wts.chat".

![](https://files.readme.io/76c4ae2777e38063a22bb3cf1ada4ee603fbc98602785c16ba4a7c7ca59a36f2-image.png)

*Visualize o ícone do aplicativo wts.chat em Aplicativos Instalados*

<br />

5. ### Crie um Novo Cenário
   Vá para a seção “Cenários”. Clique no botão “Crie um novo cenário” no canto superior direito da tela.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f6ead864644441c5328cf2630f30d8962742d533f63ea778af58321aa8a69bae-create_scenario.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]

6. ### Adicione o módulo wtsChat ao Cenário
   Após criar o cenário, um pop-up será exibido permitindo que você pesquise os aplicativos. Digite "wts chat" na barra de pesquisa. Você poderá ver todos os módulos do wts chat, organizados em grupos como “Contatos”, “Mensagens”, “Painéis”, etc.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c653eb4d846c64beefb01adf8166fa3a66824241f2e741d367cab70cce6c5cd1-INSTALAO_2.gif",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


---

# N8N

O **n8n** é uma plataforma **LowCode** que permite criar automações de maneira intuitiva, sem a necessidade de conhecimento profundo em programação. Com o n8n, é possível integrar nossa plataforma com diversos serviços externos, aumentando significativamente as possibilidades ao utilizar nossa API.

# Modalidades de uso

### n8n.cloud

Você pode optar por contratar o n8n como **serviço na nuvem**, pagando por execução dos fluxos. Existem diferentes pacotes com limites de execuções mensais, atendendo às necessidades da maioria dos usuários. Este modelo é ideal para aqueles que buscam simplicidade e não querem se preocupar com manutenção de infraestrutura.\
Veja mais [aqui](https://n8n.io).

### Auto-hospedado (Self-hosted)

Para cenários em que há grande volume de integrações e automações, o custo do n8n na nuvem pode ser um fator limitante. Nesse caso, é possível instalar o n8n em um servidor próprio, permitindo execuções ilimitadas e reduzindo os custos relacionados.

Com a opção de **auto-hospedagem**, você paga apenas pelo servidor, o que é vantajoso para quem deseja flexibilidade e escalabilidade sem restrição de execuções.\
Veja mais [aqui](https://docs.n8n.io/hosting/).

***

# Módulo nativo para uso Self-hosted

Desenvolvemos um módulo nativo para facilitar a integração;

> 📘 Atenção - Community Nodes
>
> Para construção do módulo utilizamos a funcionalidade **Community Nodes** do N8N, esta funcionalidade está disponível apenas para contas **auto-hospedadas (self-hosted)**.
>
> Os usuários com n8n.cloud ainda não têm acesso a essa funcionalidade.

### Passos para instalação

**1 - Acesse as configurações na página inicial do n8n. Para isso, clique no menu de configurações no canto inferior esquerdo, em seguida clique em “Settings”/ “Configurações”.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/71de7612ae22b4af7730ebc6dec92b7ffa7d5bd0db6ba32f4b97dfe72df00491-chrome-capture-2024-11-19_2.gif",
        "",
        "Configurações da plataforma"
      ],
      "align": "center",
      "caption": "Configurações da plataforma"
    }
  ]
}
[/block]

**2 - Em seguida, no menu de opções clique em “Community nodes”/ “Nós da comunidade”.**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0ecb7ffaaa79d7602cd7272e58fa61da6ff43b6600e4a3b961f9cbf64cf0a34a-community.png",
        "",
        "Opção \"Community nodes\""
      ],
      "align": "center",
      "caption": "Opção \"Community nodes\""
    }
  ]
}
[/block]

**3 - Clique em “Install comunnity nodes”.**

Adicione o nome do pacote npm e aceite os termos de instalação e clique em install.\
**Nome do pacote**: n8n-nodes-wts.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a0f9d80c267de39a3188e62fc2a5c59bcd504b8cd2bfe691d001824a655b4f00-Nome_NPM.png",
        "",
        "Defina o nome do pacote: **n8n-nodes-wts**"
      ],
      "align": "center",
      "caption": "Defina o nome do pacote: **n8n-nodes-wts**"
    }
  ]
}
[/block]

### 🎉 Pronto, agora é só usar...

***

### Uso do módulo

* Clique no painel de nós, no canto superior direito e busque por “wts chat” para listar as ações disponíveis.

[block:image]{"images":[{"image":["https://files.readme.io/deb34f3d8488b542c6936a683d2025997f8268ed5d76c8b67f7c962711e5523a-zoom.gif","",""],"align":"center"}]}[/block]

Para utilizar o módulo, é necessário ter um token permanente, saiba mais [aqui](https://flwchat.readme.io/reference/criar-token-para-integra%C3%A7%C3%A3o) .

Após adicionar um dos nós, clique em **Credential to connect with** e **Create new credential**. Escolha um nome que identifique a sua conta na plataforma. Para finalizar, clique em **salvar**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/bdeaf66ba592ecbe7ad27a56df035e7f89ba9ce940921788a4e361e8416fc52b-chrome-capture-2024-11-19_5.gif",
        "",
        ""
      ],
      "align": "center",
      "border": true
    }
  ]
}
[/block]

Preencha as outras opções do nó e execute.

### 🎉 Pronto você deu o primeiro passo para realizar as integrações.


---

# Referência por domínio

# Arquivos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v2/file — Obter url para upload

Envie os metadados do arquivo e você receberá uma URL e deverá fazer upload para ela usando o método PUT Após enviar o conteúdo do arquivo, faça uma chamada para o endpont POST /core/v2/file

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Type` | query | sim | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | Tipo do arquivo Se informado o tipo UNDEFINED o sistema tentará identificar o tipo do arquivo Arquivos do tipo DOCUMENT não passam por transformação ou compressão, mas arquivos do tipo IMAGE e VIDEO são transformados para que sejam compatíveis com todas as plataformas. |
| `Name` | query | sim | string | Nome do arquivo, com extensão (ex.: paisagem.jpg) |
| `MimeType` | query | - | string | Mimetype do arquivo. Se não informado ele será definido pelo tipo ou extensão do arquivo |

**Resposta 200** [`PublicUrlUploadFileV2DTO`](#publicurluploadfilev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | - | Código do arquivo temporário, só será válido após confirmar o salvamento; |
| `urlUpload` | string | - | Url para upload do arquivo (utilize o metodo PUT para upload) |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-file

## `POST` /core/v2/file — Salvar arquivo

Após o upload do arquivo na URL fornecida na rota GET /core/v2/file execute este metodo para obter o ID do arquivo O Id do arquivo pode ser fornecido no envio de mensagens. O FileId pode ser reaproveitado, não sendo necessário novos uploads para o mesmo arquivo.

**Body** [`PublicReqFileSaveV2DTO`](#publicreqfilesavev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | sim | Código do arquivo |

**Resposta 200** [`PublicFileV2DTO`](#publicfilev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | - |  |
| `key` | string | - |  |
| `size` | integer(int64) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-file

---

## Schemas

### PublicFileV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT` | - |  |
| `key` | string | - |  |
| `size` | integer(int64) | - |  |

### PublicReqFileSaveV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | sim | Código do arquivo |

### PublicUrlUploadFileV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tempFileId` | string(uuid) | - | Código do arquivo temporário, só será válido após confirmar o salvamento; |
| `urlUpload` | string | - | Url para upload do arquivo (utilize o metodo PUT para upload) |


---

# Campos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/custom-field — Listar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `EntityType` | query | - | enum: `CONTACT`, `PANEL` | Tipo de entidade do campo personalizado. |
| `NestedList` | query | - | boolean | Determina a estrutura da lista retornada. Se verdadeiro, os campos serão retornados de forma aninhada, isto é, estruturado em grupos. |

**Resposta 200** [`PublicCustomFieldDTO`](#publiccustomfielddto)[]

Array de [`PublicCustomFieldDTO`](#publiccustomfielddto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-custom-field

---

## Schemas

### PublicCustomFieldDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

### PublicCustomFieldOptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |


---

# Canais de Atendimento

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/channel — Listar

Listagem de canais de atendimento.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `ChannelType` | query | - | enum: `All`, `Whatsapp`, `Messenger`, `Instagram` | Tipo do canal. |

**Resposta 200** [`PublicChannelDTO`](#publicchanneldto)[]

Array de [`PublicChannelDTO`](#publicchanneldto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `type` | enum: `Dialog360_WhatsApp`, `CloudAPI_WhatsApp`, `ZAPI_WhatsApp`, `EvolutionApi_WhatsApp`, `Instagram`, `Messenger` | - |  |
| `number` | string | - |  |
| `numberFormatted` | string | - |  |
| `identity` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-channel

---

## Schemas

### PublicChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `type` | enum: `Dialog360_WhatsApp`, `CloudAPI_WhatsApp`, `ZAPI_WhatsApp`, `EvolutionApi_WhatsApp`, `Instagram`, `Messenger` | - |  |
| `number` | string | - |  |
| `numberFormatted` | string | - |  |
| `identity` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |

### PublicChannelIdentityDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `humanId` | string | - |  |
| `platform` | string | - |  |
| `provider` | string | - |  |
| `providerVariable` | string | - |  |
| `pictureUrl` | string | - |  |
| `displayName` | string | - |  |


---

# Cards

Serviço `crm` — base `https://api.wts.chat/crm`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /crm/v1/panel/card/{cardId}/note — Listar anotações

Listagem paginada de anotações.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `cardId` | path | sim | string(uuid) | ID do card. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicPanelCardNoteDTOPublicPageListDTO`](#publicpanelcardnotedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardNoteDTO`](#publicpanelcardnotedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-panel-card-cardid-note

## `POST` /crm/v1/panel/card/{cardId}/note — Adicionar anotação

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `cardId` | path | sim | string(uuid) | ID do card. |

**Body** [`PublicReqCreatePanelNoteDTO`](#publicreqcreatepanelnotedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da anotação. |
| `fileUrls` | string[] | - | URL pública de algum arquivo que deseja-se anexar à anotação. O tamanho máximo permitido para um arquivo é de 25MB. |

**Resposta 200** [`PublicPanelCardNoteDTO`](#publicpanelcardnotedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `cardId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `text` | string | - |  |
| `files` | [`PublicFileDTO`](#publicfiledto)[] | - |  |
| `isFromPublicApi` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-panel-card-cardid-note

## `DELETE` /crm/v1/panel/card/{cardId}/note/{noteId} — Remover anotação

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `cardId` | path | sim | string(uuid) | ID do card. |
| `noteId` | path | sim | string(uuid) | ID da anotação. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-panel-card-cardid-note-noteid

## `GET` /crm/v2/panel/card — Listar

Listagem paginada de cards.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `PanelId` | query | sim | string(uuid) | ID do painel. |
| `StepId` | query | - | string(uuid) | Filtro por ID da etapa. |
| `ContactId` | query | - | string(uuid) | Filtro por ID do contato. |
| `ResponsibleUserId` | query | - | string(uuid) | Filtro por ID do responsável. |
| `TextFilter` | query | - | string | Filtro textual. A busca é realizada nos atributos textuais relevantes do item. |
| `IncludeDetails` | query | - | enum: `PanelTitle`, `StepTitle`, `StepPhase`, `ResponsibleUser`, `Contacts`, `CustomFields`, `LostReason`[] | Detalhes que devem ser incluídos na resposta. |
| `Statuses` | query | - | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED`[] | Filtro por situação do card. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicPanelCardDTOV2PublicPageListDTO`](#publicpanelcarddtov2publicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-panel-card

## `POST` /crm/v2/panel/card — Criar

**Body** [`PublicReqCreatePanelCardDTO`](#publicreqcreatepanelcarddto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `stepId` | string(uuid) | sim | ID da etapa do painel onde o item deverá ser inserido. |
| `title` | string | sim | Título do item. |
| `description` | string | - | Descrição do item. |
| `position` | number(double) | - | Posição do item na etapa. |
| `dueDate` | string(date-time) | - | Data de vencimento do item. |
| `responsibleUserId` | string(uuid) | - | ID do usuário responsável pelo item. |
| `tagIds` | string(uuid)[] | - | IDss das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `contactIds` | string[] | - | IDs dos contatos relacionados ao item. |
| `sessionId` | string(uuid) | - | ID da conversa relacionada ao item. |
| `monetaryAmount` | number(double) | - | Valor monetário atribuído ao item. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no item. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o item. Neste campo, pode ser salvo qualquer propriedade adicional para o item, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste item, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste item, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |

**Resposta 200** [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - |  |
| `lostReason` | [`LostReasonDTO`](#lostreasondto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-panel-card

## `GET` /crm/v2/panel/card/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do card. |
| `IncludeDetails` | query | - | enum: `PanelTitle`, `StepTitle`, `StepPhase`, `ResponsibleUser`, `Contacts`, `CustomFields`, `LostReason`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - |  |
| `lostReason` | [`LostReasonDTO`](#lostreasondto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-panel-card-id

## `POST` /crm/v2/panel/card/{id}/duplicate — Duplicar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do card. |

**Body** [`PublicReqDuplicatePanelCardDTO`](#publicreqduplicatepanelcarddto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `copyToStepId` | string(uuid) | - | ID da etapa de destino, pode ser uma etapa do mesmo painel ou de outro painel. Se vazio, mantem a cópia na mesma etapa. |
| `options` | [`PublicReqDuplicateOptionsPanelCardDTO`](#publicreqduplicateoptionspanelcarddto) | - |  |

**Resposta 200** [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - |  |
| `lostReason` | [`LostReasonDTO`](#lostreasondto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-panel-card-id-duplicate

## `PUT` /crm/v3/panel/card/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string | ID do card. |

**Body** [`PublicReqUpdatePanelCardDTO`](#publicrequpdatepanelcarddto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `StepId`, `Title`, `Description`, `Position`, `DueDate`, `ResponsibleUserId`, `TagIds`, `ContactIds`, `SessionId`, `MonetaryAmount`, `Archived`, `CustomFields` … (+2)[] | - | Campos a serem atualizados. |
| `stepId` | string(uuid) | - | ID da etapa do painel para onde o item deverá ser movido. |
| `title` | string | - | Título do item. |
| `description` | string | - | Descrição do item. |
| `position` | number(double) | - | Posição do item na etapa. |
| `dueDate` | string(date-time) | - | Data de vencimento do item. |
| `responsibleUserId` | string(uuid) | - | ID do usuário responsável pelo item. |
| `tagIds` | string(uuid)[] | - | IDss das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `contactIds` | string(uuid)[] | - | IDs dos contatos relacionados ao item. |
| `sessionId` | string(uuid) | - | ID da conversa relacionada ao item. |
| `monetaryAmount` | number(double) | - | Valor monetário atribuído ao item. |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - | Determina o status do item. |
| `lostReasonId` | string(uuid) | - | ID do motivo de perda. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no item. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o item. Neste campo, pode ser salvo qualquer propriedade adicional para o item, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste item, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste item, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqUpdatePanelCardOptionsDTO`](#publicrequpdatepanelcardoptionsdto) | - |  |

**Resposta 200** [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - |  |
| `lostReason` | [`LostReasonDTO`](#lostreasondto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v3-panel-card-id

---

## Schemas

### LostReasonDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicFileDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO` | - |  |
| `publicUrl` | string | - |  |
| `publicUrlDownload` | string | - |  |
| `size` | integer(int64) | - |  |
| `isThumbnail` | boolean | - |  |
| `thumbnail` | [`PublicFileThumbnailDTO`](#publicfilethumbnaildto) | - |  |

### PublicFileThumbnailDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `publicUrl` | string | - |  |

### PublicPanelCardContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicPanelCardDTOV2

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - |  |
| `lostReason` | [`LostReasonDTO`](#lostreasondto) | - |  |

### PublicPanelCardDTOV2PublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardDTOV2`](#publicpanelcarddtov2)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPanelCardNoteDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `cardId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `text` | string | - |  |
| `files` | [`PublicFileDTO`](#publicfiledto)[] | - |  |
| `isFromPublicApi` | boolean | - |  |

### PublicPanelCardNoteDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardNoteDTO`](#publicpanelcardnotedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPanelCardResponsibleUserDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicReqCreatePanelCardDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `stepId` | string(uuid) | sim | ID da etapa do painel onde o item deverá ser inserido. |
| `title` | string | sim | Título do item. |
| `description` | string | - | Descrição do item. |
| `position` | number(double) | - | Posição do item na etapa. |
| `dueDate` | string(date-time) | - | Data de vencimento do item. |
| `responsibleUserId` | string(uuid) | - | ID do usuário responsável pelo item. |
| `tagIds` | string(uuid)[] | - | IDss das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `contactIds` | string[] | - | IDs dos contatos relacionados ao item. |
| `sessionId` | string(uuid) | - | ID da conversa relacionada ao item. |
| `monetaryAmount` | number(double) | - | Valor monetário atribuído ao item. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no item. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o item. Neste campo, pode ser salvo qualquer propriedade adicional para o item, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste item, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste item, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |

### PublicReqCreatePanelNoteDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da anotação. |
| `fileUrls` | string[] | - | URL pública de algum arquivo que deseja-se anexar à anotação. O tamanho máximo permitido para um arquivo é de 25MB. |

### PublicReqDuplicateOptionsPanelCardDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `archiveOriginalCard` | boolean | - | Arquiva item original |
| `fields` | enum: `Undefined`, `All`, `Amount`, `DueDate`, `Tags`, `MonetaryAmount`, `Contacts`, `ResponsibleUser`, `CustomFields`, `Notes`[] | - | Campos que devem ser incluídos da duplicação, se vazio copiará tudo. |

### PublicReqDuplicatePanelCardDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `copyToStepId` | string(uuid) | - | ID da etapa de destino, pode ser uma etapa do mesmo painel ou de outro painel. Se vazio, mantem a cópia na mesma etapa. |
| `options` | [`PublicReqDuplicateOptionsPanelCardDTO`](#publicreqduplicateoptionspanelcarddto) | - |  |

### PublicReqUpdatePanelCardDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `StepId`, `Title`, `Description`, `Position`, `DueDate`, `ResponsibleUserId`, `TagIds`, `ContactIds`, `SessionId`, `MonetaryAmount`, `Archived`, `CustomFields` … (+2)[] | - | Campos a serem atualizados. |
| `stepId` | string(uuid) | - | ID da etapa do painel para onde o item deverá ser movido. |
| `title` | string | - | Título do item. |
| `description` | string | - | Descrição do item. |
| `position` | number(double) | - | Posição do item na etapa. |
| `dueDate` | string(date-time) | - | Data de vencimento do item. |
| `responsibleUserId` | string(uuid) | - | ID do usuário responsável pelo item. |
| `tagIds` | string(uuid)[] | - | IDss das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `contactIds` | string(uuid)[] | - | IDs dos contatos relacionados ao item. |
| `sessionId` | string(uuid) | - | ID da conversa relacionada ao item. |
| `monetaryAmount` | number(double) | - | Valor monetário atribuído ao item. |
| `status` | enum: `OPEN`, `WON`, `LOST`, `ARCHIVED` | - | Determina o status do item. |
| `lostReasonId` | string(uuid) | - | ID do motivo de perda. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no item. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o item. Neste campo, pode ser salvo qualquer propriedade adicional para o item, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste item, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste item, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqUpdatePanelCardOptionsDTO`](#publicrequpdatepanelcardoptionsdto) | - |  |

### PublicReqUpdatePanelCardOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `upsertTagOperation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Defina como deve ser realizada a alteração no campo Etiquetas: InsertIfNotExists: insere apenas etiquetas que ainda não estão no card. DeleteIfExists: remove apenas etiquetas que já estão no card. ReplaceAll: remove todas as etiquetas e inclui apenas as informadas (padrão). |


---

# Carteiras

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/portfolio — Listar

Listagem paginada de carteiras.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `IncludeDetails` | query | - | enum: `Departments`, `ContactCount`[] |  |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicPortfolioDTOPublicPageListDTO`](#publicportfoliodtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPortfolioDTO`](#publicportfoliodto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-portfolio

## `DELETE` /core/v1/portfolio/{id}/contact — Remover contato

Remova um contato de uma carteira.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | Id da carteira. |

**Body** [`PublicRequestContactPortfolioDTO`](#publicrequestcontactportfoliodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - |  |
| `phoneNumber` | string | - |  |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-portfolio-id-contact

## `GET` /core/v1/portfolio/{id}/contact — Listar contatos

Listagem de contatos associados a uma carteira.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | Id da carteira. |
| `CreatedAt.Before` | query | - | string(date-time) |  |
| `CreatedAt.After` | query | - | string(date-time) |  |
| `CreatedAt.ApplyCompanyTimezone` | query | - | boolean |  |
| `CreatedAt.IsNull` | query | - | boolean |  |
| `UpdatedAt.Before` | query | - | string(date-time) |  |
| `UpdatedAt.After` | query | - | string(date-time) |  |
| `UpdatedAt.ApplyCompanyTimezone` | query | - | boolean |  |
| `UpdatedAt.IsNull` | query | - | boolean |  |
| `ContactIds` | query | - | string(uuid)[] |  |
| `Page` | query | - | integer(int32) |  |
| `PageSize` | query | - | integer(int32) |  |
| `OrderBy` | query | - | string |  |
| `OrderByDesc` | query | - | string |  |
| `TimestampField` | query | - | string |  |
| `TimestampFilter` | query | - | string(date-time) |  |
| `NextPageToken` | query | - | string |  |
| `Type` | query | - | enum: `Undefined`, `PageNumber`, `Timestamp`, `Token` |  |
| `SkipCount` | query | - | boolean |  |

**Resposta 200** [`PublicContactPortfolioDTOPublicPageListDTO`](#publiccontactportfoliodtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactPortfolioDTO`](#publiccontactportfoliodto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-portfolio-id-contact

## `POST` /core/v1/portfolio/{id}/contact — Adicionar contato

Adicione um contato em uma carteira.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | Id da carteira. |

**Body** [`PublicRequestContactPortfolioDTO`](#publicrequestcontactportfoliodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - |  |
| `phoneNumber` | string | - |  |

**Resposta 200** [`PublicContactPortfolioDTO`](#publiccontactportfoliodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `companyId` | string(uuid) | - |  |
| `portfolioId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactDetails` | [`PublicContactDetailsPortfolioDTO`](#publiccontactdetailsportfoliodto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-portfolio-id-contact

## `DELETE` /core/v1/portfolio/{id}/contact/batch — Remover contatos

Remova contatos de uma carteira adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | Id da carteira. |

**Body** [`PublicRequestContactsPortfolioDTO`](#publicrequestcontactsportfoliodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - |  |
| `phoneNumbers` | string[] | - |  |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-portfolio-id-contact-batch

## `POST` /core/v1/portfolio/{id}/contact/batch — Adicionar contatos

Adicione contatos em uma carteira adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | Id da carteira. |

**Body** [`PublicRequestContactsPortfolioDTO`](#publicrequestcontactsportfoliodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - |  |
| `phoneNumbers` | string[] | - |  |

**Resposta 200** [`PublicContactPortfolioDTOPublicPageListDTO`](#publiccontactportfoliodtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactPortfolioDTO`](#publiccontactportfoliodto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-portfolio-id-contact-batch

---

## Schemas

### PublicContactDetailsPortfolioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |
| `phonenumber` | string | - |  |
| `phonenumberFormatted` | string | - |  |
| `instagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `email` | string | - |  |
| `annotation` | string | - |  |

### PublicContactPortfolioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `companyId` | string(uuid) | - |  |
| `portfolioId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactDetails` | [`PublicContactDetailsPortfolioDTO`](#publiccontactdetailsportfoliodto) | - |  |

### PublicContactPortfolioDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactPortfolioDTO`](#publiccontactportfoliodto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPortfolioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `automaticAttribution` | boolean | - |  |
| `expirationDurationInMonths` | integer(int32) | - |  |
| `contactsCount` | integer(int32) | - |  |
| `type` | enum: `MULTIPLE`, `SINGLE` | - |  |
| `departments` | [`PublicPortfolioDepartmentDTO`](#publicportfoliodepartmentdto)[] | - |  |

### PublicPortfolioDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPortfolioDTO`](#publicportfoliodto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPortfolioDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `departmentId` | string(uuid) | - |  |
| `userIds` | string(uuid)[] | - |  |

### PublicRequestContactPortfolioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - |  |
| `phoneNumber` | string | - |  |

### PublicRequestContactsPortfolioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - |  |
| `phoneNumbers` | string[] | - |  |


---

# Chatbots

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/chatbot — Listar

Listagem de chatbots.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Name` | query | - | string | Filtro por nome do chatbot. |
| `Types` | query | - | enum: `Reactive`, `Automation`[] | Filtro por tipo de uso do chatbot. É possível informar mais de um tipo. |
| `ChannelIds` | query | - | string(uuid)[] | Filtro por ID do canal. É possível informar mais de um ID. |
| `DefaultDepartmentIds` | query | - | string(uuid)[] | Filtro por ID da equipe padrão. É possível informar mais de um ID. |
| `PublishStatuses` | query | - | enum: `Not_Published`, `Publishing`, `Ready`, `Failed`[] | Filtro por status de publicação do chatbot. É possível informar mais de um status. |
| `AutomationUsages` | query | - | enum: `Api`, `Manual`, `Campaign`, `Sequence`[] | Filtro por disponibilidade da automação. É possível informar mais de uma disponibilidade. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicChatbotDTOPublicPageListDTO`](#publicchatbotdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicChatbotDTO`](#publicchatbotdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-chatbot

## `POST` /chat/v1/chatbot/send — Enviar chatbot

Permite iniciar a execução de um chatbot. Durante a execução do chatbot, a interação com a conversa fica desabilitada para atendentes na central de atendimento. A execução pode ser cancelada a qualquer momento, via API ou através da central de atendimento. Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio.

**Body** [`PublicReqSendBotDTO`](#publicreqsendbotdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | - | Chave do chatbot a ser enviado. |
| `from` | string | - | Número de telefone ou @usuarioinstagram do canal cadastrado na conta. |
| `to` | string | - | Número de telefone ou @usuarioinstagram do destinatário. |
| `sessionId` | string(uuid) | - | ID da conversa para a qual o chatbot deve ser enviado. Se a conversa estiver concluída, o chatbot será executado sem reiniciá-la. |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `sessionMetadata` | object | - | Metadados relevantes para o atendimento. Através deste campo, é possível salvar propriedades adicionais para o atendimento, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são enviados apenas enquanto o atendimento estiver ativo, ou seja, não são enviados em atendimentos posteriores. |
| `contactMetadata` | object | - | Metadados relevantes para o contato. Através deste campo, é possível salvar propriedades adicionais para o contato, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são salvos no contato e, portanto, são enviados mesmo em atendimentos posteriores. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta do disparo. |
| `callbackUrl` | string | - | URL para receber webhook quando o chatbot for iniciado ou falhar. |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-chatbot-send

---

## Schemas

### PublicAgentDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `phoneNumber` | string | - |  |
| `email` | string | - |  |
| `pictureFileId` | string(uuid) | - |  |
| `pictureUrl` | string | - |  |

### PublicChannelIdentityDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `humanId` | string | - |  |
| `platform` | string | - |  |
| `provider` | string | - |  |
| `providerVariable` | string | - |  |
| `pictureUrl` | string | - |  |
| `displayName` | string | - |  |

### PublicChatbotDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `key` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `archived` | boolean | - |  |
| `name` | string | - |  |
| `type` | enum: `Reactive`, `Automation` | - |  |
| `channelIds` | string(uuid)[] | - |  |
| `defaultDepartmentId` | string(uuid) | - |  |
| `publishStatus` | enum: `NOT_PUBLISHED`, `PUBLISHING`, `READY`, `FAILED` | - |  |
| `automationUsage` | enum: `Api`, `Manual`, `Campaign`, `Sequence`[] | - |  |

### PublicChatbotDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicChatbotDTO`](#publicchatbotdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicContactDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |
| `pictureUrl` | string | - |  |
| `phonenumber` | string | - |  |
| `instagram` | string | - |  |
| `phonenumberFormatted` | string | - |  |
| `tagsId` | string(uuid)[] | - |  |
| `tagsName` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED`, `UNDEFINED` | - |  |

### PublicDepartmentDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `description` | string | - |  |
| `isDefault` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicReqSendBotDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | - | Chave do chatbot a ser enviado. |
| `from` | string | - | Número de telefone ou @usuarioinstagram do canal cadastrado na conta. |
| `to` | string | - | Número de telefone ou @usuarioinstagram do destinatário. |
| `sessionId` | string(uuid) | - | ID da conversa para a qual o chatbot deve ser enviado. Se a conversa estiver concluída, o chatbot será executado sem reiniciá-la. |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `sessionMetadata` | object | - | Metadados relevantes para o atendimento. Através deste campo, é possível salvar propriedades adicionais para o atendimento, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são enviados apenas enquanto o atendimento estiver ativo, ou seja, não são enviados em atendimentos posteriores. |
| `contactMetadata` | object | - | Metadados relevantes para o contato. Através deste campo, é possível salvar propriedades adicionais para o contato, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são salvos no contato e, portanto, são enviados mesmo em atendimentos posteriores. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta do disparo. |
| `callbackUrl` | string | - | URL para receber webhook quando o chatbot for iniciado ou falhar. |

### PublicReqSendBotOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `skipIfBotInExecution` | boolean | - | Se outro chatbot estiver em execução, o chatbot não será enviado. |
| `skipIfInProgress` | boolean | - | Se uma conversa estiver em andamento, o chatbot não será enviado. |
| `forceStartSession` | boolean | - | Se uma conversa estiver em andamento, ela será concluída e uma nova será iniciada. |
| `hiddenSession` | boolean | - | Determina se o atendimento deve estar oculto na tela. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. O atendimento passará a ser visível caso o contato responda. |

### PublicSessionClassificationDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `category` | enum: `UNDEFINED`, `WON`, `LOST`, `INFO`, `OTHER` | - |  |
| `categoryDescription` | string | - |  |
| `amount` | number(double) | - |  |
| `categoryName` | string | - |  |

### PublicSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

### PublicUtmDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sourceId` | string | - |  |
| `source` | string | - |  |
| `clid` | string | - |  |
| `medium` | string | - |  |
| `campaign` | string | - |  |
| `content` | string | - |  |
| `headline` | string | - |  |
| `term` | string | - |  |
| `referralUrl` | string | - |  |


---

# Contatos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/contact — Listar

Listagem paginada de contatos. Para resultados mais específicos, utilize o endpoint `/filter`.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |
| `Status` | query | - | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicContactDTOPublicPageListDTO`](#publiccontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact

## `POST` /core/v1/contact — Criar

**Body** [`PublicReqCreateContactIndividualDTO`](#publicreqcreatecontactindividualdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact

## `GET` /core/v1/contact/custom-field — Campos personalizados

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `NestedList` | query | - | boolean | Determina a estrutura da lista retornada. Se verdadeiro, os campos serão retornados de forma aninhada, isto é, estruturado em grupos. |

**Resposta 200** [`PublicCustomFieldDTO`](#publiccustomfielddto)[]

Array de [`PublicCustomFieldDTO`](#publiccustomfielddto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact-custom-field

## `POST` /core/v1/contact/filter — Filtrar

Filtragem paginada de contatos.

**Body** [`PublicReqFilterContactDTO`](#publicreqfiltercontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `createdAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `updatedAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `includeDetails` | enum: `Tags`, `CustomFields`, `Portfolios`[] | - | Detalhes que devem ser incluídos na resposta. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `textFilter` | string | - | Filtro textual. A busca é realizada nos atributos textuais relevantes do contato. |
| `name` | string | - | Filtro por nome. |
| `phoneNumber` | string | - | Filtro por número de telefone. |
| `email` | string | - | Filtro por email. |
| `instagram` | string | - | Filtro por nome de usuário do Instagram. |
| `tagIds` | string(uuid)[] | - | Filtro por etiquetas usando IDs. |
| `tagNames` | string[] | - | Filtro por etiquetas usando nomes. |
| `portfolioIds` | string(uuid)[] | - | Filtro por carteiras usando IDs. |
| `portfolioNames` | string[] | - | Filtro por carteiras usando nomes. |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - | Filtro por origem. |
| `customFields` | object | - | Filtro por valores de campos personalizados. |
| `metadata` | object | - | Filtro por metadados. |

**Resposta 200** [`PublicContactDTOPublicPageListDTO`](#publiccontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-filter

## `GET` /core/v1/contact/phonenumber/{phone} — Obter por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone |
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact-phonenumber-phone

## `PUT` /core/v1/contact/phonenumber/{phone} — Atualizar por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone. |

**Body** [`PublicReqUpdateContactDTO`](#publicrequpdatecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-contact-phonenumber-phone

## `POST` /core/v1/contact/phonenumber/{phone}/tags — Atualizar etiquetas por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone |

**Body** [`PublicReqUpdateContactTagDTO`](#publicrequpdatecontacttagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-phonenumber-phone-tags

## `GET` /core/v1/contact/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato |
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact-id

## `POST` /core/v1/contact/{id}/tags — Atualizar etiquetas

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato ou número de telefone. |

**Body** [`PublicReqUpdateContactTagDTO`](#publicrequpdatecontacttagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-id-tags

## `POST` /core/v2/contact/batch — Salvar em massa

Permite salvar até 100 contatos em uma única requisição. Se um contato com o mesmo número de telefone, Instagram ou endereço de email já existir, este apenas será atualizado.

**Body** [`PublicReqBatchCreateContactV2DTO`](#publicreqbatchcreatecontactv2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `items` | [`PublicReqCreateContactDTO`](#publicreqcreatecontactdto)[] | sim | Dados para criação dos contatos. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)[]

Array de [`PublicContactDTO`](#publiccontactdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-contact-batch

## `PUT` /core/v2/contact/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato. |

**Body** [`PublicReqUpdateContactDTO`](#publicrequpdatecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v2-contact-id

---

## Schemas

### PublicContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

### PublicContactDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicCustomFieldDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

### PublicCustomFieldOptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicDateFilterDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `before` | string(date-time) | - | Limite superior de busca, sempre em fuso horário UTM. |
| `after` | string(date-time) | - | Limite inferior de busca, sempre em fuso horário UTM. |

### PublicReqBatchCreateContactV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `items` | [`PublicReqCreateContactDTO`](#publicreqcreatecontactdto)[] | sim | Dados para criação dos contatos. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

### PublicReqContactUpdatePartialOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagsOperation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Define como as listas de tags devem ser tratadas ao atualizar, como padrão será InsertIfNotExists |

### PublicReqCreateContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |

### PublicReqCreateContactIndividualDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

### PublicReqCreateContactOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `upsert` | boolean | - | Com esta opção habilitada, se o contato já existir na base de dados, ele será atualizado com os novos dados e retornado. |
| `upsertFields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Defina quais campos deverão ser motificados em caso de upsert (quando o contato já existe), se não for informado todos os campos serão afetados |
| `upsertTagOperation` | enum: `INSERTIFNOTEXISTS`, `DELETEIFEXISTS`, `REPLACEALL` | - | Defina como deve ser a alteração no campo Etiquetas em caso de upsert(quando o contato já existe) InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. (Opção padrão) |
| `getIfExists` | boolean | - | Com esta opção habilitada, se o contato já existir na base de dados, ele será retornado e nenhum dado será atualizado; |

### PublicReqFilterContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `createdAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `updatedAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `includeDetails` | enum: `Tags`, `CustomFields`, `Portfolios`[] | - | Detalhes que devem ser incluídos na resposta. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `textFilter` | string | - | Filtro textual. A busca é realizada nos atributos textuais relevantes do contato. |
| `name` | string | - | Filtro por nome. |
| `phoneNumber` | string | - | Filtro por número de telefone. |
| `email` | string | - | Filtro por email. |
| `instagram` | string | - | Filtro por nome de usuário do Instagram. |
| `tagIds` | string(uuid)[] | - | Filtro por etiquetas usando IDs. |
| `tagNames` | string[] | - | Filtro por etiquetas usando nomes. |
| `portfolioIds` | string(uuid)[] | - | Filtro por carteiras usando IDs. |
| `portfolioNames` | string[] | - | Filtro por carteiras usando nomes. |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - | Filtro por origem. |
| `customFields` | object | - | Filtro por valores de campos personalizados. |
| `metadata` | object | - | Filtro por metadados. |

### PublicReqUpdateContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

### PublicReqUpdateContactTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

### PublicUtmDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sourceId` | string | - |  |
| `source` | string | - |  |
| `clid` | string | - |  |
| `medium` | string | - |  |
| `campaign` | string | - |  |
| `content` | string | - |  |
| `headline` | string | - |  |
| `term` | string | - |  |
| `referralUrl` | string | - |  |


---

# Conversas

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `DELETE` /chat/v1/session/note/{id} — Excluir uma nota interna

Este endpoint permite a exclusão de uma nota interna por meio de seu ID.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-session-note-id

## `GET` /chat/v1/session/note/{id} — Obter uma nota interna

Este endpoint permite a obtenção de uma nota interna por meio de seu ID.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-session-note-id

## `PUT` /chat/v1/session/{id}/assignee — Atribuir usuário

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |

**Body** [`PublicReqAssignUserSessionDTO`](#publicreqassignusersessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | sim | ID do usuário. |
| `options` | [`PublicTransferSessionOptionsDTO`](#publictransfersessionoptionsdto) | - |  |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-session-id-assignee

## `PUT` /chat/v1/session/{id}/complete — Concluir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |

**Body** [`PublicReqCompleteSessionDTO`](#publicreqcompletesessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `reactivateOnNewMessage` | boolean | - | Determina se a conversa deve ser reativada ao receber uma nova mensagem do contato. O valor padrão é `false`. |
| `stopBotInExecution` | boolean | - | Determina se o chatbot de automação em execução deve ser interrompido. O valor padrão é `false`. |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-session-id-complete

## `GET` /chat/v1/session/{id}/message — Listar mensagens

Listagem paginada de mensagens por ID de uma conversa.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicMessageDTOPublicPageListDTO`](#publicmessagedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicMessageDTO`](#publicmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-session-id-message

## `POST` /chat/v1/session/{id}/message — Enviar mensagem

Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio. O envio da mensagem será assincrono, ao enviar a mensagem será salva em uma fila de disparo, e será processada posteriormente. Para verificar a situação do envio, consulte pelo endereço /chat/v1/message/{}/status

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Body** [`PublicQuickSendBodyDTO`](#publicquicksendbodydto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `templateId` ou `fileUrl`. |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `text` ou `fileUrl`. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `fileUrl` | string | - | URL pública de algum arquivo que deseja-se enviar na mensagem. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `fileId` | string(uuid) | - | Código do arquivo que deseja-se enviar na mensagem, o ID pode ser obtido nas rotas /core/v2/file, o arquivo deverá seguir as regras do canal de atendimento. |
| `refId` | string(uuid) | - | ID de referência para identificar a mensagem externamente como resposta a uma mensagem anterior. |

**Resposta 200** [`PublicQuickMessageDTO`](#publicquickmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `statusUrl` | string | - |  |
| `failureReason` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-session-id-message

## `POST` /chat/v1/session/{id}/message/sync — Enviar mensagem síncrona

Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio. O envio da mensagem será síncrono, então ele pode demorar um tempo até que o servidor do canal de atencimento responda com um status válido para a mensagem. O tempo máximo que este metodo esperará uma resposta é de 25 segundos, após este tempo ele entregará a última situação da mensagem;

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Body** [`PublicQuickSendBodyDTO`](#publicquicksendbodydto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `templateId` ou `fileUrl`. |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `text` ou `fileUrl`. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `fileUrl` | string | - | URL pública de algum arquivo que deseja-se enviar na mensagem. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `fileId` | string(uuid) | - | Código do arquivo que deseja-se enviar na mensagem, o ID pode ser obtido nas rotas /core/v2/file, o arquivo deverá seguir as regras do canal de atendimento. |
| `refId` | string(uuid) | - | ID de referência para identificar a mensagem externamente como resposta a uma mensagem anterior. |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-session-id-message-sync

## `GET` /chat/v1/session/{id}/note — Listar notas internas

Este endpoint permite a listagem de notas internas de um atendimento.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicMessageDTOPublicPageListDTO`](#publicmessagedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicMessageDTO`](#publicmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-session-id-note

## `POST` /chat/v1/session/{id}/note — Salvar nota interna

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Body** [`PublicNoteSendBodyDTO`](#publicnotesendbodydto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem |
| `filesUrls` | string[] | - | Lista de arquivos (Urls) |
| `filesIds` | string(uuid)[] | - | Lista de arquivos (Ids) |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-session-id-note

## `PUT` /chat/v1/session/{id}/status — Alterar status

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |

**Body** [`PublicReqChangeStatusSessionDTO`](#publicreqchangestatussessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `newStatus` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | sim | Novo status para a conversa. |
| `options` | [`PublicChangeStatusSessionOptionsDTO`](#publicchangestatussessionoptionsdto) | - |  |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-session-id-status

## `PUT` /chat/v1/session/{id}/transfer — Transferir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |

**Body** [`PublicReqTransferSessionDTO`](#publicreqtransfersessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `type` | enum: `DEPARTMENT`, `USER` | sim | Determina se a transferência deverá ser entre equipes ou usuários. |
| `newDepartmentId` | string(uuid) | - | ID da nova equipe para a conversa. |
| `newUserId` | string(uuid) | - | ID do novo usuário para a conversa. |
| `options` | [`PublicTransferSessionOptionsDTO`](#publictransfersessionoptionsdto) | - |  |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-session-id-transfer

## `GET` /chat/v2/session — Listar

Listagem paginada de conversas.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Status` | query | - | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN`[] | Filtro por status da conversa. |
| `DepartmentId` | query | - | string(uuid) | Filtro por ID da equipe. |
| `UserId` | query | - | string(uuid) | Filtro por ID do usuário. |
| `TagsId` | query | - | string(uuid)[] | Filtro por IDs de etiquetas |
| `TagsName` | query | - | string[] | Filtro por nomes de etiquetas |
| `ChannelsId` | query | - | string(uuid)[] | Filtro por ID de canais |
| `ContactId` | query | - | string(uuid) | Filtro por ID do contato. |
| `EndAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `EndAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `ActiveAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `ActiveAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `LastInteractionAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `LastInteractionAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `IncludeDetails` | query | - | enum: `Undefined`, `AgentDetails`, `DepartmentsDetails`, `ContactDetails`, `ChannelTypeDetails`, `ClassificationDetails`, `ChannelDetails`[] | Inclua detalhes de outras entidades no resultado da sua busca. |
| `Metadata` | query | - | object | Filtro por metadados. |
| `Type` | query | - | enum: `INDIVIDUAL`, `GROUP` | Filtro por tipo da conversa. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicSessionDTOV2PublicPageListDTO`](#publicsessiondtov2publicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSessionDTOV2`](#publicsessiondtov2)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-session

## `GET` /chat/v2/session/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |
| `includeDetails` | query | - | enum: `Undefined`, `AgentDetails`, `DepartmentsDetails`, `ContactDetails`, `ChannelTypeDetails`, `ClassificationDetails`, `ChannelDetails`[] |  |

**Resposta 200** [`PublicSessionDTOV2`](#publicsessiondtov2)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |
| `type` | enum: `INDIVIDUAL`, `GROUP` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-session-id

## `PUT` /chat/v2/session/{id}/partial — Alterar

Atualiza um ou mais atributos de uma conversa. Para usar você deve informar o novo valor do atribuito e quais atributos serão atualizados.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da conversa. |

**Body** [`PublicReqUpdatePartialSessionDTO`](#publicrequpdatepartialsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `companyId` | string(uuid) | - | Código da empresa |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - | Situação do atendmento |
| `endAt` | string(date-time) | - | Data de conclusão |
| `number` | string | - | Código de identificação |
| `departmentId` | string(uuid) | - | Código da equipe |
| `userId` | string(uuid) | - | Código do usuário / atendente |
| `classification` | [`PublicReqUpdatePartialSessionClassificationDTO`](#publicrequpdatepartialsessionclassificationdto) | - |  |
| `metadata` | object | - | Definição dos metadados |
| `options` | [`PublicUpdatePartialSessionOptionsDTO`](#publicupdatepartialsessionoptionsdto) | - |  |
| `fields` | enum: `Status`, `EndAt`, `UserId`, `DepartmentId`, `ReactivateDisabled`, `Autocomplete`, `Number`, `Metadata`, `Classification`[] | - | Definição dos campos a serem atualizados |

**Resposta 200** [`PublicSessionDTO`](#publicsessiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v2-session-id-partial

---

## Schemas

### PublicAgentDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `phoneNumber` | string | - |  |
| `email` | string | - |  |
| `pictureFileId` | string(uuid) | - |  |
| `pictureUrl` | string | - |  |

### PublicChangeStatusSessionOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `stopBotInExecution` | boolean | - | Determina se o chatbot de automação em execução deve ser interrompido. O valor padrão é `false`. |

### PublicChannelIdentityDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `humanId` | string | - |  |
| `platform` | string | - |  |
| `provider` | string | - |  |
| `providerVariable` | string | - |  |
| `pictureUrl` | string | - |  |
| `displayName` | string | - |  |

### PublicContactDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |
| `pictureUrl` | string | - |  |
| `phonenumber` | string | - |  |
| `instagram` | string | - |  |
| `phonenumberFormatted` | string | - |  |
| `tagsId` | string(uuid)[] | - |  |
| `tagsName` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED`, `UNDEFINED` | - |  |

### PublicDepartmentDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `description` | string | - |  |
| `isDefault` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicFileDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO` | - |  |
| `publicUrl` | string | - |  |
| `publicUrlDownload` | string | - |  |
| `size` | integer(int64) | - |  |
| `isThumbnail` | boolean | - |  |
| `thumbnail` | [`PublicFileThumbnailDTO`](#publicfilethumbnaildto) | - |  |

### PublicFileThumbnailDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `publicUrl` | string | - |  |

### PublicMessageContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |

### PublicMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

### PublicMessageDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicMessageDTO`](#publicmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicMessageDetailsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `file` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `files` | [`PublicFileDTO`](#publicfiledto)[] | - |  |
| `fileAsLink` | [`PublicMessageFileAsLinkDTO`](#publicmessagefileaslinkdto) | - |  |
| `location` | [`PublicMessageLocationDTO`](#publicmessagelocationdto) | - |  |
| `contact` | [`PublicMessageContactDTO`](#publicmessagecontactdto) | - |  |
| `errors` | [`PublicMessageErrorDTO`](#publicmessageerrordto)[] | - |  |
| `footerText` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `payTransactionId` | string(uuid) | - |  |
| `reactionToContact` | enum: `SMILE`, `SAD`, `WOW`, `LOVE` | - |  |
| `reactionFromContact` | string | - |  |
| `track` | [`PublicMessageTrackDTO`](#publicmessagetrackdto) | - |  |
| `transcription` | [`PublicMsgTranscriptionDTO`](#publicmsgtranscriptiondto) | - |  |
| `templateCategoryId` | string(uuid) | - |  |
| `templateCategoryName` | string | - |  |
| `waitReply` | boolean | - |  |

### PublicMessageErrorDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `date` | string(date-time) | - |  |
| `origin` | string | - |  |
| `key` | string | - |  |
| `text` | string | - |  |

### PublicMessageFileAsLinkDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `file` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `shortUrl` | string | - |  |

### PublicMessageLocationDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `latitude` | number(double) | - |  |
| `longitude` | number(double) | - |  |
| `address` | string | - |  |
| `name` | string | - |  |
| `url` | string | - |  |

### PublicMessageTrackDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `type` | enum: `ACCESS_PAGE`, `START_CHAT`, `SAVE_CONTACT` | - |  |
| `pageTitle` | string | - |  |
| `pageUrl` | string | - |  |
| `pageUtm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `isMobileDevice` | boolean | - |  |
| `formData` | [`PublicMessageTrackFromDataDTO`](#publicmessagetrackfromdatadto) | - |  |

### PublicMessageTrackFromDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `annotation` | string | - |  |

### PublicMsgTranscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - |  |
| `processing` | boolean | - |  |
| `error` | boolean | - |  |

### PublicNoteSendBodyDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem |
| `filesUrls` | string[] | - | Lista de arquivos (Urls) |
| `filesIds` | string(uuid)[] | - | Lista de arquivos (Ids) |

### PublicQuickMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `statusUrl` | string | - |  |
| `failureReason` | string | - |  |

### PublicQuickSendBodyDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `templateId` ou `fileUrl`. |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `text` ou `fileUrl`. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `fileUrl` | string | - | URL pública de algum arquivo que deseja-se enviar na mensagem. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `fileId` | string(uuid) | - | Código do arquivo que deseja-se enviar na mensagem, o ID pode ser obtido nas rotas /core/v2/file, o arquivo deverá seguir as regras do canal de atendimento. |
| `refId` | string(uuid) | - | ID de referência para identificar a mensagem externamente como resposta a uma mensagem anterior. |

### PublicReqAssignUserSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | sim | ID do usuário. |
| `options` | [`PublicTransferSessionOptionsDTO`](#publictransfersessionoptionsdto) | - |  |

### PublicReqChangeStatusSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `newStatus` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | sim | Novo status para a conversa. |
| `options` | [`PublicChangeStatusSessionOptionsDTO`](#publicchangestatussessionoptionsdto) | - |  |

### PublicReqCompleteSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `reactivateOnNewMessage` | boolean | - | Determina se a conversa deve ser reativada ao receber uma nova mensagem do contato. O valor padrão é `false`. |
| `stopBotInExecution` | boolean | - | Determina se o chatbot de automação em execução deve ser interrompido. O valor padrão é `false`. |

### PublicReqTransferSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `type` | enum: `DEPARTMENT`, `USER` | sim | Determina se a transferência deverá ser entre equipes ou usuários. |
| `newDepartmentId` | string(uuid) | - | ID da nova equipe para a conversa. |
| `newUserId` | string(uuid) | - | ID do novo usuário para a conversa. |
| `options` | [`PublicTransferSessionOptionsDTO`](#publictransfersessionoptionsdto) | - |  |

### PublicReqUpdatePartialSessionClassificationDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `description` | string | - | Descrição da classificação da conclusão |
| `category` | enum: `UNDEFINED`, `WON`, `LOST`, `INFO`, `OTHER` | - | Categoria da classificação da conclusão |
| `amount` | number(double) | - | Valor atribuído à classificação da conclusão |

### PublicReqUpdatePartialSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `companyId` | string(uuid) | - | Código da empresa |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - | Situação do atendmento |
| `endAt` | string(date-time) | - | Data de conclusão |
| `number` | string | - | Código de identificação |
| `departmentId` | string(uuid) | - | Código da equipe |
| `userId` | string(uuid) | - | Código do usuário / atendente |
| `classification` | [`PublicReqUpdatePartialSessionClassificationDTO`](#publicrequpdatepartialsessionclassificationdto) | - |  |
| `metadata` | object | - | Definição dos metadados |
| `options` | [`PublicUpdatePartialSessionOptionsDTO`](#publicupdatepartialsessionoptionsdto) | - |  |
| `fields` | enum: `Status`, `EndAt`, `UserId`, `DepartmentId`, `ReactivateDisabled`, `Autocomplete`, `Number`, `Metadata`, `Classification`[] | - | Definição dos campos a serem atualizados |

### PublicSessionClassificationDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `category` | enum: `UNDEFINED`, `WON`, `LOST`, `INFO`, `OTHER` | - |  |
| `categoryDescription` | string | - |  |
| `amount` | number(double) | - |  |
| `categoryName` | string | - |  |

### PublicSessionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |

### PublicSessionDTOV2

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `startAt` | string(date-time) | - |  |
| `endAt` | string(date-time) | - |  |
| `status` | enum: `UNDEFINED`, `STARTED`, `PENDING`, `IN_PROGRESS`, `COMPLETED`, `HIDDEN` | - |  |
| `companyId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `channelId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `previewUrl` | string | - |  |
| `title` | string | - |  |
| `number` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `origin` | string | - |  |
| `contactDetails` | [`PublicContactDataDTO`](#publiccontactdatadto) | - |  |
| `agentDetails` | [`PublicAgentDataDTO`](#publicagentdatadto) | - |  |
| `channelDetails` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |
| `departmentDetails` | [`PublicDepartmentDataDTO`](#publicdepartmentdatadto) | - |  |
| `classification` | [`PublicSessionClassificationDTO`](#publicsessionclassificationdto) | - |  |
| `statusDescription` | string | - |  |
| `timeService` | string | - |  |
| `timeWait` | string | - |  |
| `firstResponseAt` | string(date-time) | - |  |
| `botId` | string(uuid) | - |  |
| `unreadCount` | integer(int32) | - |  |
| `lastMessageText` | string | - |  |
| `lastInteractionDate` | string(date-time) | - |  |
| `lastMessageOut` | string(date-time) | - |  |
| `lastMessageIn` | string(date-time) | - |  |
| `windowStatus` | enum: `ACTIVE`, `EXPIRED`, `NOT_STARTED` | - |  |
| `metadata` | object | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |
| `type` | enum: `INDIVIDUAL`, `GROUP` | - |  |

### PublicSessionDTOV2PublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSessionDTOV2`](#publicsessiondtov2)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicTransferSessionOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `stopBotInExecution` | boolean | - | Determina se o chatbot de automação em execução deve ser interrompido. O valor padrão é `false`. |

### PublicUpdatePartialSessionOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `stopBotInExecution` | boolean | - | Determina se o chatbot de automação em execução deve ser interrompido. O valor padrão é `false`. |

### PublicUtmDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sourceId` | string | - |  |
| `source` | string | - |  |
| `clid` | string | - |  |
| `medium` | string | - |  |
| `campaign` | string | - |  |
| `content` | string | - |  |
| `headline` | string | - |  |
| `term` | string | - |  |
| `referralUrl` | string | - |  |


---

# Envios (Msg/Otp/Bot)

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `POST` /chat/v1/send/audio — Áudio

Envia uma mensagem de áudio para um contato. O campo FileIdOrUrl é obrigatório; informe uma URL pública ou o ID de um arquivo previamente cadastrado. O arquivo deve seguir as regras do canal de atendimento (formato e tamanho). O campo CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendMediaAudioDTO`](#publicreqsendmediaaudiodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-audio

## `POST` /chat/v1/send/chatbot — Chatbot

Enfileira o disparo de um chatbot para um contato. O processamento ocorre de forma assíncrona após o retorno deste endpoint. Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendBotDTO`](#publicreqsendbotdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | - | Chave do chatbot a ser enviado. |
| `from` | string | - | Número de telefone ou @usuarioinstagram do canal cadastrado na conta. |
| `to` | string | - | Número de telefone ou @usuarioinstagram do destinatário. |
| `sessionId` | string(uuid) | - | ID da conversa para a qual o chatbot deve ser enviado. Se a conversa estiver concluída, o chatbot será executado sem reiniciá-la. |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `sessionMetadata` | object | - | Metadados relevantes para o atendimento. Através deste campo, é possível salvar propriedades adicionais para o atendimento, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são enviados apenas enquanto o atendimento estiver ativo, ou seja, não são enviados em atendimentos posteriores. |
| `contactMetadata` | object | - | Metadados relevantes para o contato. Através deste campo, é possível salvar propriedades adicionais para o contato, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são salvos no contato e, portanto, são enviados mesmo em atendimentos posteriores. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta do disparo. |
| `callbackUrl` | string | - | URL para receber webhook quando o chatbot for iniciado ou falhar. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-chatbot

## `POST` /chat/v1/send/chatbot/batch — Chatbot (em lote)

Enfileira o disparo de um chatbot para múltiplos contatos em uma única requisição. O campo BotKey é compartilhado por todos os destinatários. Cada item da lista deve conter o destinatário (To) ou o ID da conversa (SessionId). O processamento ocorre de forma assíncrona após o retorno deste endpoint. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendBotBatchDTO`](#publicreqsendbotbatchdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | sim | Chave do chatbot a ser enviado para todos os destinatários. |
| `from` | string | - | Canal de origem (Id do canal ou número do WhatsApp ou @usuarioinstagram). |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `messages` | [`PublicReqSendBotBatchItemDTO`](#publicreqsendbotbatchitemdto)[] | sim | Lista de destinatários. |

**Resposta 200** [`PublicRespSendMessagesDTO`](#publicrespsendmessagesdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `results` | [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-chatbot-batch

## `GET` /chat/v1/send/chatbot/{id} — Chatbot status

Consulta o status atual de um disparo de chatbot enfileirado anteriormente pelos endpoints de envio. O parâmetro id aceita o ID retornado no momento do envio. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string | ID do disparo para consultar o status. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-send-chatbot-id

## `POST` /chat/v1/send/document — Documento

Envia uma mensagem de documento para um contato. O campo FileIdOrUrl é obrigatório; informe uma URL pública ou o ID de um arquivo previamente cadastrado. O arquivo deve seguir as regras do canal de atendimento (formato e tamanho). O campo CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendMediaDocumentDTO`](#publicreqsendmediadocumentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-document

## `POST` /chat/v1/send/image — Imagem

Envia uma mensagem de imagem para um contato. O campo FileIdOrUrl é obrigatório; informe uma URL pública ou o ID de um arquivo previamente cadastrado. O arquivo deve seguir as regras do canal de atendimento (formato e tamanho). O campo CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendMediaImageDTO`](#publicreqsendmediaimagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-image

## `GET` /chat/v1/send/message/{id} — Mensagem status

Consulta o status atual de uma mensagem enviada anteriormente pelos endpoints de envio. O parâmetro id aceita o ID da mensagem retornado no momento do envio. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string | ID da mensagem para consultar o status. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-send-message-id

## `POST` /chat/v1/send/otp — OTP

Envia uma senha OTP para um contato no WhatsApp. OTP = One time password. O campo Code é opcional; se não informado, será gerado um código de 5 dígitos aleatórios. O campo SenderId pode ser usado para controle do seu sistema. O CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendOtpMessageV2DTO`](#publicreqsendotpmessagev2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `code` | string | - | Código a ser enviado. Caso não seja informado, um código aleatório será gerado. |
| `templateId` | string | - | ID do modelo de mensagem do tipo Autenticação |
| `from` | string | sim | Número do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for entregue ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |

**Resposta 200** [`PublicRespSendOtpMessageDTO`](#publicrespsendotpmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `code` | string | - |  |
| `status` | enum: `UNDEFINED`, `PENDING`, `SENT`, `RECEIVED`, `FAILED` | - |  |
| `from` | string | - |  |
| `templateId` | string | - |  |
| `companyId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `channelId` | string(uuid) | - |  |
| `sentAt` | string(date-time) | - |  |
| `receivedAt` | string(date-time) | - |  |
| `contactPhoneNumber` | string | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `statusUrl` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-otp

## `GET` /chat/v1/send/otp/{id} — OTP status

Consulta o status atual de uma mensagem OTP enviada anteriormente. O parâmetro id aceita o ID da mensagem ou o SenderId informado no envio. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string | ID da mensagem ou SenderId para consultar o status. |

**Resposta 200** [`PublicSendOtpStatusDTO`](#publicsendotpstatusdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `code` | string | - |  |
| `status` | enum: `UNDEFINED`, `PENDING`, `SENT`, `RECEIVED`, `FAILED` | - |  |
| `templateId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `channelId` | string(uuid) | - |  |
| `sentAt` | string(date-time) | - |  |
| `receivedAt` | string(date-time) | - |  |
| `contactPhoneNumber` | string | - |  |
| `statusUrl` | string | - |  |
| `failedReason` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-send-otp-id

## `POST` /chat/v1/send/template — Modelo

Envia um modelo de mensagem para um único destinatário. O campo TemplateId é obrigatório e deve corresponder a um template cadastrado no canal. O campo Parameters deve ser preenchido caso o template possua variáveis. O campo FileIdOrUrl é necessário apenas para templates com mídia. O CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendTemplateSingleDTO`](#publicreqsendtemplatesingledto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | sim |  |
| `from` | string | sim |  |
| `templateId` | string | sim | ID do modelo de mensagem a ser enviado. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o template possua variáveis. |
| `fileIdOrUrl` | string | - | URL pública ou ID de um arquivo a ser enviado junto ao template. O arquivo deve seguir as regras do canal de atendimento. |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar. |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `sessionMetadata` | object | - | Metadados do atendimento na estrutura chave-valor. Utilizáveis como parâmetros no chatbot e enviados de volta nos webhooks. Válidos apenas enquanto o atendimento estiver ativo. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-template

## `POST` /chat/v1/send/template/batch — Modelo (em lote)

Envia um modelo de mensagem para múltiplos destinatários em uma única requisição. O campo TemplateId é compartilhado por todos os destinatários. Cada item da lista deve conter o destinatário (To) e pode ter parâmetros e arquivo próprios. O campo FileIdOrUrl por item é necessário apenas para templates com mídia. O CallbackUrl por item permite receber webhook individual por mensagem. As opções (User, Department, EnableBot, etc.) se aplicam a todos os atendimentos criados no lote. É possível enviar até 100 mensagens por requisição. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendTemplateBatchDTO`](#publicreqsendtemplatebatchdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | sim |  |
| `templateId` | string | sim | ID do modelo de mensagem a ser enviado para todos os destinatários. |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `messages` | [`PublicReqSendTemplateBatchItemDTO`](#publicreqsendtemplatebatchitemdto)[] | sim | Lista de destinatários e respectivos parâmetros. |

**Resposta 200** [`PublicRespSendMessagesDTO`](#publicrespsendmessagesdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `results` | [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-template-batch

## `POST` /chat/v1/send/text — Texto

Envia uma mensagem de texto simples para um contato. O campo Text é obrigatório. O campo DelayTyping simula o indicador "digitando..." por até 25 segundos antes de entregar a mensagem. O campo CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendTextDTO`](#publicreqsendtextdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `text` | string | sim | Texto da mensagem a ser enviada. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-text

## `POST` /chat/v1/send/typing — Digitando

Envia o indicador de "digitando" para o contato da conversa informada. **Disponível apenas para canais CloudAPI (WhatsApp Business API oficial).** Para outros tipos de canal, a requisição é aceita porém não produz efeito.

**Body** [`PublicReqSendTypingDTO`](#publicreqsendtypingdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionId` | string(uuid) | sim | ID da sessão ativa para enviar o indicador de digitação. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-typing

## `POST` /chat/v1/send/video — Vídeo

Envia uma mensagem de vídeo para um contato. O campo FileIdOrUrl é obrigatório; informe uma URL pública ou o ID de um arquivo previamente cadastrado. O arquivo deve seguir as regras do canal de atendimento (formato e tamanho). O campo CallbackUrl permite receber webhook quando a mensagem for entregue ou falhar. Este endpoint tem rate limit individual e permite 1000 requisições a cada 2 minutos.

**Body** [`PublicReqSendMediaVideoDTO`](#publicreqsendmediavideodto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

**Resposta 200** [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-send-video

---

## Schemas

### PublicReqSendBotBatchDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | sim | Chave do chatbot a ser enviado para todos os destinatários. |
| `from` | string | - | Canal de origem (Id do canal ou número do WhatsApp ou @usuarioinstagram). |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `messages` | [`PublicReqSendBotBatchItemDTO`](#publicreqsendbotbatchitemdto)[] | sim | Lista de destinatários. |

### PublicReqSendBotBatchItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - | Número de telefone ou @usuarioinstagram do destinatário. Obrigatório se SessionId não for informado. |
| `sessionId` | string(uuid) | - | ID da conversa para a qual o chatbot deve ser enviado. Obrigatório se To não for informado. |
| `sessionMetadata` | object | - | Metadados do atendimento na estrutura chave-valor. Utilizáveis como parâmetros no chatbot e enviados de volta nos webhooks. Válidos apenas enquanto o atendimento estiver ativo. |
| `contactMetadata` | object | - | Metadados do contato na estrutura chave-valor. Utilizáveis como parâmetros no chatbot e enviados de volta nos webhooks. Salvos no contato e enviados em atendimentos futuros. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta do disparo. |
| `callbackUrl` | string | - | URL para receber webhook quando o chatbot for iniciado ou falhar. |

### PublicReqSendBotDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `botKey` | string(uuid) | - | Chave do chatbot a ser enviado. |
| `from` | string | - | Número de telefone ou @usuarioinstagram do canal cadastrado na conta. |
| `to` | string | - | Número de telefone ou @usuarioinstagram do destinatário. |
| `sessionId` | string(uuid) | - | ID da conversa para a qual o chatbot deve ser enviado. Se a conversa estiver concluída, o chatbot será executado sem reiniciá-la. |
| `options` | [`PublicReqSendBotOptionsDTO`](#publicreqsendbotoptionsdto) | - |  |
| `sessionMetadata` | object | - | Metadados relevantes para o atendimento. Através deste campo, é possível salvar propriedades adicionais para o atendimento, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são enviados apenas enquanto o atendimento estiver ativo, ou seja, não são enviados em atendimentos posteriores. |
| `contactMetadata` | object | - | Metadados relevantes para o contato. Através deste campo, é possível salvar propriedades adicionais para o contato, na estrutura chave-valor. Qualquer metadado adicionado poderá ser utilizado como parâmetro nas mensagens e condicionais do chatbot, além de serem enviados de volta nos webhooks. Esses metadados são salvos no contato e, portanto, são enviados mesmo em atendimentos posteriores. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta do disparo. |
| `callbackUrl` | string | - | URL para receber webhook quando o chatbot for iniciado ou falhar. |

### PublicReqSendBotOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `skipIfBotInExecution` | boolean | - | Se outro chatbot estiver em execução, o chatbot não será enviado. |
| `skipIfInProgress` | boolean | - | Se uma conversa estiver em andamento, o chatbot não será enviado. |
| `forceStartSession` | boolean | - | Se uma conversa estiver em andamento, ela será concluída e uma nova será iniciada. |
| `hiddenSession` | boolean | - | Determina se o atendimento deve estar oculto na tela. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. O atendimento passará a ser visível caso o contato responda. |

### PublicReqSendDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | ID da equipe a ser atribuída ao atendimento. |
| `name` | string | - | Nome da equipe a ser atribuída ao atendimento. |

### PublicReqSendMediaAudioDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |

### PublicReqSendMediaDocumentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

### PublicReqSendMediaImageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

### PublicReqSendMediaVideoDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `fileIdOrUrl` | string | sim | Informe uma URL (com acesso público) do arquivo ou o Id de um arquivo. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `text` | string | - | Legenda a ser enviada junto com o arquivo. O suporte a legenda depende do canal de atendimento. |

### PublicReqSendOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `enableBot` | boolean | - | Determina se o chatbot deve ser ativado ao receber uma resposta do contato. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. |
| `hiddenSession` | boolean | - | Determina se o atendimento deve estar oculto na tela. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. O atendimento passará a ser visível caso o contato responda. |
| `forceStartSession` | boolean | - | Se um atendimento estiver em andamento, força o encerramento dele e inicia um novo. |
| `user` | [`PublicReqSendUserDTO`](#publicreqsenduserdto) | - |  |
| `department` | [`PublicReqSendDepartmentDTO`](#publicreqsenddepartmentdto) | - |  |

### PublicReqSendOtpMessageV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `code` | string | - | Código a ser enviado. Caso não seja informado, um código aleatório será gerado. |
| `templateId` | string | - | ID do modelo de mensagem do tipo Autenticação |
| `from` | string | sim | Número do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for entregue ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |

### PublicReqSendTemplateBatchDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | sim |  |
| `templateId` | string | sim | ID do modelo de mensagem a ser enviado para todos os destinatários. |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `messages` | [`PublicReqSendTemplateBatchItemDTO`](#publicreqsendtemplatebatchitemdto)[] | sim | Lista de destinatários e respectivos parâmetros. |

### PublicReqSendTemplateBatchItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | sim |  |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o template possua variáveis. |
| `fileIdOrUrl` | string | - | URL pública ou ID de um arquivo a ser enviado junto ao template. O arquivo deve seguir as regras do canal de atendimento. |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar. |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `sessionMetadata` | object | - | Metadados do atendimento na estrutura chave-valor. Utilizáveis como parâmetros no chatbot e enviados de volta nos webhooks. Válidos apenas enquanto o atendimento estiver ativo. |

### PublicReqSendTemplateSingleDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | sim |  |
| `from` | string | sim |  |
| `templateId` | string | sim | ID do modelo de mensagem a ser enviado. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o template possua variáveis. |
| `fileIdOrUrl` | string | - | URL pública ou ID de um arquivo a ser enviado junto ao template. O arquivo deve seguir as regras do canal de atendimento. |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar. |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `sessionMetadata` | object | - | Metadados do atendimento na estrutura chave-valor. Utilizáveis como parâmetros no chatbot e enviados de volta nos webhooks. Válidos apenas enquanto o atendimento estiver ativo. |

### PublicReqSendTextDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `to` | string | - |  |
| `from` | string | - |  |
| `options` | [`PublicReqSendOptionsDTO`](#publicreqsendoptionsdto) | - |  |
| `sessionId` | string(uuid) | - | ID do atendimento. (Opcional) Deve ser utilizado para atendimentos em tempo real, como respostas de IA externa. |
| `refId` | string(uuid) | - | ID da mensagem que está sendo respondida. Para resposta a uma mensagem |
| `delayTyping` | integer(int32) | - | Tempo em segundos "digitando..." antes de entregar a mensagem. Se fornecido o disparo será adiado, para que o contato consiga ver o digitando. Para a API Oficial, utilize o endpoint específico para uma melhor experiência Max.: 25 segundos |
| `callbackUrl` | string | - | URL para receber webhook quando a mensagem for enviada ou falhar |
| `senderId` | string | - | ID de identificação no seu sistema para rastreamento e consulta da mensagem. |
| `text` | string | sim | Texto da mensagem a ser enviada. |

### PublicReqSendTypingDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionId` | string(uuid) | sim | ID da sessão ativa para enviar o indicador de digitação. |

### PublicReqSendUserDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | ID do atendente a ser atribuído ao atendimento. |
| `phoneNumber` | string | - | Telefone do atendente a ser atribuído ao atendimento. |
| `email` | string | - | E-mail do atendente a ser atribuído ao atendimento. |

### PublicRespSendMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `senderId` | string | - |  |
| `statusUrl` | string | - |  |
| `sentAt` | string(date-time) | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `waitReply` | boolean | - |  |

### PublicRespSendMessagesDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `results` | [`PublicRespSendMessageDTO`](#publicrespsendmessagedto)[] | - |  |

### PublicRespSendOtpMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `code` | string | - |  |
| `status` | enum: `UNDEFINED`, `PENDING`, `SENT`, `RECEIVED`, `FAILED` | - |  |
| `from` | string | - |  |
| `templateId` | string | - |  |
| `companyId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `channelId` | string(uuid) | - |  |
| `sentAt` | string(date-time) | - |  |
| `receivedAt` | string(date-time) | - |  |
| `contactPhoneNumber` | string | - |  |
| `failedReason` | string | - |  |
| `callbackUrl` | string | - |  |
| `statusUrl` | string | - |  |

### PublicSendOtpStatusDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `code` | string | - |  |
| `status` | enum: `UNDEFINED`, `PENDING`, `SENT`, `RECEIVED`, `FAILED` | - |  |
| `templateId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `channelId` | string(uuid) | - |  |
| `sentAt` | string(date-time) | - |  |
| `receivedAt` | string(date-time) | - |  |
| `contactPhoneNumber` | string | - |  |
| `statusUrl` | string | - |  |
| `failedReason` | string | - |  |


---

# Equipes

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `POST` /core/v1/department — Criar

**Body** [`PublicReqSaveDepartmentDTO`](#publicreqsavedepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `agents` | [`PublicDepartmentAgentCreateDTO`](#publicdepartmentagentcreatedto)[] | - | Lista de usuários para criar na equipe |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-department

## `DELETE` /core/v1/department/{id} — Excluir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-department-id

## `GET` /core/v1/department/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |
| `includeDetails` | query | - | enum: `All`, `Agents`, `Channels` |  |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-department-id

## `PUT` /core/v1/department/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe. |

**Body** [`PublicReqUpdateDepartmentDTO`](#publicrequpdatedepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `fields` | enum: `Name`, `Description`, `IsDefault`, `DistributionIsEnabled`, `ChannelsConfig`, `RestrictionType`, `DistributionConfig`[] | sim | Campos que devem ser atualizados |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-department-id

## `PUT` /core/v1/department/{id}/agents — Atualizar usuários

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe |

**Body** [`PublicReqUpdateDepartmentAgent`](#publicrequpdatedepartmentagent)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

**Resposta 200** [`PublicReqUpdateDepartmentAgent`](#publicrequpdatedepartmentagent)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-department-id-agents

## `GET` /core/v1/department/{id}/channel — Listar canais

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe |

**Resposta 200** [`PublicDepartmentListChannelDTO`](#publicdepartmentlistchanneldto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - |  |
| `channels` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-department-id-channel

## `GET` /core/v2/department — Listar

**Resposta 200** [`PublicDepartmentDTOV2`](#publicdepartmentdtov2)[]

Array de [`PublicDepartmentDTOV2`](#publicdepartmentdtov2).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-department

---

## Schemas

### DepartmentChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `number` | string | - |  |
| `name` | string | - |  |
| `type` | string | - |  |

### DepartmentDetailsDistributionConfigDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `expirationIsEnabled` | boolean | - |  |
| `maximumDurationInMinutes` | integer(int32) | - |  |
| `inactivityTimeInMinutes` | integer(int32) | - |  |

### PublicAgentUpdateDepartmentItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicDepartmentAgentCreateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | sim | ID do usuário |
| `isAgent` | boolean | - | Se é atendente na equipe |
| `isSupervisor` | boolean | - | Se é supervisor na equipe |

### PublicDepartmentAgentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicDepartmentChannelsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - | Escopo de canais permitidos |
| `channels` | string[] | - | ID, nome ou numero dos canais permitidos (quando escopo é SELECTED) |

### PublicDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

### PublicDepartmentDTOV2

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |

### PublicDepartmentListChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - |  |
| `channels` | string(uuid)[] | - |  |

### PublicReqSaveDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `agents` | [`PublicDepartmentAgentCreateDTO`](#publicdepartmentagentcreatedto)[] | - | Lista de usuários para criar na equipe |

### PublicReqUpdateDepartmentAgent

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

### PublicReqUpdateDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `fields` | enum: `Name`, `Description`, `IsDefault`, `DistributionIsEnabled`, `ChannelsConfig`, `RestrictionType`, `DistributionConfig`[] | sim | Campos que devem ser atualizados |


---

# Etiquetas

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/tag — Listar

**Resposta 200** [`PublicTagDTO`](#publictagdto)[]

Array de [`PublicTagDTO`](#publictagdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-tag

## `POST` /core/v1/tag — Criar

Cria uma etiqueta na conta. A cor define automaticamente a cor do texto; quando omitida, a etiqueta é criada em `GRAY_600`.

**Body** [`PublicReqCreateTagDTO`](#publicreqcreatetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a etiqueta é criada em `GRAY_600`. Use `GET /v1/tag/color` para as cores disponíveis. |

**Resposta 200** [`PublicTagDTO`](#publictagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-tag

## `GET` /core/v1/tag/color — Listar cores

Listagem das cores disponíveis para etiquetas. O valor de `color` é o que deve ser informado na criação e na atualização.

**Resposta 200** [`PublicTagColorDTO`](#publictagcolordto)[]

Array de [`PublicTagColorDTO`](#publictagcolordto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cores disponíveis para etiquetas. O nome combina a família de cor com o tom, do mais claro (100) ao mais escuro (600). |
| `bgColor` | string | - | Cor de fundo da etiqueta, em hexadecimal. |
| `textColor` | string | - | Cor do texto correspondente, em hexadecimal. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-tag-color

## `DELETE` /core/v1/tag/{id} — Excluir

Exclui uma etiqueta. Quando a etiqueta estiver vinculada a contatos, a exclusão é recusada até que seja confirmada com `removeFromContacts`, pois ela será removida de todos os contatos associados.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da etiqueta. |

**Body** [`PublicReqDeleteTagDTO`](#publicreqdeletetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `removeFromContacts` | boolean | - | Confirma a exclusão de uma etiqueta que está vinculada a contatos, removendo-a de todos eles. Sem esta confirmação, a exclusão é recusada quando existir ao menos um contato vinculado. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-tag-id

## `PUT` /core/v1/tag/{id} — Atualizar

Atualiza o nome e a cor de uma etiqueta. Quando a cor é omitida, a cor atual é mantida.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da etiqueta. |

**Body** [`PublicReqUpdateTagDTO`](#publicrequpdatetagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a cor atual da etiqueta é mantida. Use `GET /v1/tag/color` para as cores disponíveis. |

**Resposta 200** [`PublicTagDTO`](#publictagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-tag-id

---

## Schemas

### PublicReqCreateTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a etiqueta é criada em `GRAY_600`. Use `GET /v1/tag/color` para as cores disponíveis. |

### PublicReqDeleteTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `removeFromContacts` | boolean | - | Confirma a exclusão de uma etiqueta que está vinculada a contatos, removendo-a de todos eles. Sem esta confirmação, a exclusão é recusada quando existir ao menos um contato vinculado. |

### PublicReqUpdateTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome da etiqueta. |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. A cor do texto é definida automaticamente a partir dela. Quando omitida, a cor atual da etiqueta é mantida. Use `GET /v1/tag/color` para as cores disponíveis. |

### PublicTagColorDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cores disponíveis para etiquetas. O nome combina a família de cor com o tom, do mais claro (100) ao mais escuro (600). |
| `bgColor` | string | - | Cor de fundo da etiqueta, em hexadecimal. |
| `textColor` | string | - | Cor do texto correspondente, em hexadecimal. |

### PublicTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `color` | enum: `BROWN_100`, `BROWN_200`, `BROWN_300`, `BROWN_400`, `BROWN_500`, `BROWN_600`, `PURPLE_100`, `PURPLE_200`, `PURPLE_300`, `PURPLE_400`, `PURPLE_500`, `PURPLE_600` … (+42) | - | Cor da etiqueta. Nulo quando a etiqueta usa uma cor que não pertence à paleta da plataforma. |


---

# Horários de Atendimento

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/company/officehours — Obter

**Resposta 200** [`PublicCompanyOfficeHoursDTO`](#publiccompanyofficehoursdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `limitHours` | boolean | - | Indica se há limite de horário de atendimento |
| `offlineResponse` | string | - | Mensagem exibida quando a empresa está fora do horário de atendimento |
| `timezoneDiff` | number(double) | - | Diferença de fuso horário em relação ao UTC (em horas) |
| `days` | [`PublicCompanyOfficeHoursDayDTO`](#publiccompanyofficehoursdaydto)[] | - | Configurações de horário por dia da semana |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-company-officehours

---

## Schemas

### PublicCompanyOfficeHoursDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `limitHours` | boolean | - | Indica se há limite de horário de atendimento |
| `offlineResponse` | string | - | Mensagem exibida quando a empresa está fora do horário de atendimento |
| `timezoneDiff` | number(double) | - | Diferença de fuso horário em relação ao UTC (em horas) |
| `days` | [`PublicCompanyOfficeHoursDayDTO`](#publiccompanyofficehoursdaydto)[] | - | Configurações de horário por dia da semana |

### PublicCompanyOfficeHoursDayDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do registro |
| `dayWeek` | string | - | Dia da semana em inglês (MAIÚSCULO) |
| `active` | boolean | - | Indica se o atendimento está ativo neste dia |
| `periods` | [`PublicCompanyOfficeHoursPeriodDTO`](#publiccompanyofficehoursperioddto)[] | - | Lista de períodos de atendimento (entrada e saída) |

### PublicCompanyOfficeHoursPeriodDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `startTime` | string | - | Horário de início do período (formato HH:mm) |
| `endTime` | string | - | Horário de término do período (formato HH:mm) |


---

# Mensagens

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/message — Listar

Listagem paginada de mensagens por ID de uma conversa.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `SessionId` | query | sim | string(uuid) | ID da conversa. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicMessageDTOPublicPageListDTO`](#publicmessagedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicMessageDTO`](#publicmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-message

## `POST` /chat/v1/message/send — Enviar

Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio. O envio da mensagem será assincrono, ao enviar a mensagem será salva em uma fila de disparo, e será processada posteriormente. Para verificar a situação do envio, consulte pelo endereço /chat/v1/message/{id}/status

**Body** [`PublicReqQuickSendMessageDTO`](#publicreqquicksendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `body` | [`PublicQuickSendBodyDTO`](#publicquicksendbodydto) | sim |  |
| `department` | [`PublicQuickSendDepartmentDTO`](#publicquicksenddepartmentdto) | - |  |
| `user` | [`PublicQuickSendUserDTO`](#publicquicksenduserdto) | - |  |
| `options` | [`PublicQuickSendOptionsDTO`](#publicquicksendoptionsdto) | - |  |

**Resposta 200** [`PublicQuickMessageDTO`](#publicquickmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `statusUrl` | string | - |  |
| `failureReason` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-message-send

## `POST` /chat/v1/message/send-sync — Enviar síncrono

Este endpoint segue as mesmas regras do canal de atendimento, por exemplo: uma conversa só pode ser iniciada no WhatsApp utilizando um modelo de mensagem. Caso o contato não esteja cadastrado, ele será cadastrado automaticamente antes do envio. O envio da mensagem será síncrono, então ele pode demorar um tempo até que o servidor do canal de atencimento responda com um status válido para a mensagem. O tempo máximo que este metodo esperará uma resposta é de 25 segundos, após este tempo ele entregará a última situação da mensagem;

**Body** [`PublicReqQuickSendMessageDTO`](#publicreqquicksendmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `body` | [`PublicQuickSendBodyDTO`](#publicquicksendbodydto) | sim |  |
| `department` | [`PublicQuickSendDepartmentDTO`](#publicquicksenddepartmentdto) | - |  |
| `user` | [`PublicQuickSendUserDTO`](#publicquicksenduserdto) | - |  |
| `options` | [`PublicQuickSendOptionsDTO`](#publicquicksendoptionsdto) | - |  |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-message-send-sync

## `DELETE` /chat/v1/message/{id} — Excluir mensagem

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem a ser excluída. |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-message-id

## `GET` /chat/v1/message/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem. |

**Resposta 200** [`PublicMessageDTO`](#publicmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-message-id

## `GET` /chat/v1/message/{id}/status — Obter status por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem. |

**Resposta 200** [`PublicMessageQuickSendDTO`](#publicmessagequicksenddto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `failureReason` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-message-id-status

---

## Schemas

### PublicFileDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO` | - |  |
| `publicUrl` | string | - |  |
| `publicUrlDownload` | string | - |  |
| `size` | integer(int64) | - |  |
| `isThumbnail` | boolean | - |  |
| `thumbnail` | [`PublicFileThumbnailDTO`](#publicfilethumbnaildto) | - |  |

### PublicFileThumbnailDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `publicUrl` | string | - |  |

### PublicMessageContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |

### PublicMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `timestamp` | string(date-time) | - |  |
| `type` | enum: `TEXT`, `STICKER`, `IMAGE`, `AUDIO`, `VIDEO`, `DOCUMENT`, `CONTACT`, `LOCATION`, `LIST`, `BUTTONS`, `TRANSITION`, `TRACK` … (+1) | - |  |
| `senderId` | string | - |  |
| `sessionId` | string(uuid) | - |  |
| `templateId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `direction` | enum: `FROM_HUB`, `TO_HUB` | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `origin` | enum: `DEFAULT`, `CAMPAIGN`, `OFFICE_HOURS`, `BOT`, `API`, `PAYMENT`, `GATEWAY` | - |  |
| `text` | string | - |  |
| `fileId` | string(uuid) | - |  |
| `refId` | string(uuid) | - |  |
| `readContactAt` | string(date-time) | - |  |
| `details` | [`PublicMessageDetailsDTO`](#publicmessagedetailsdto) | - |  |
| `failedReason` | string | - |  |
| `filesIds` | string(uuid)[] | - |  |

### PublicMessageDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicMessageDTO`](#publicmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicMessageDetailsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `file` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `files` | [`PublicFileDTO`](#publicfiledto)[] | - |  |
| `fileAsLink` | [`PublicMessageFileAsLinkDTO`](#publicmessagefileaslinkdto) | - |  |
| `location` | [`PublicMessageLocationDTO`](#publicmessagelocationdto) | - |  |
| `contact` | [`PublicMessageContactDTO`](#publicmessagecontactdto) | - |  |
| `errors` | [`PublicMessageErrorDTO`](#publicmessageerrordto)[] | - |  |
| `footerText` | string | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `payTransactionId` | string(uuid) | - |  |
| `reactionToContact` | enum: `SMILE`, `SAD`, `WOW`, `LOVE` | - |  |
| `reactionFromContact` | string | - |  |
| `track` | [`PublicMessageTrackDTO`](#publicmessagetrackdto) | - |  |
| `transcription` | [`PublicMsgTranscriptionDTO`](#publicmsgtranscriptiondto) | - |  |
| `templateCategoryId` | string(uuid) | - |  |
| `templateCategoryName` | string | - |  |
| `waitReply` | boolean | - |  |

### PublicMessageErrorDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `date` | string(date-time) | - |  |
| `origin` | string | - |  |
| `key` | string | - |  |
| `text` | string | - |  |

### PublicMessageFileAsLinkDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `file` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `shortUrl` | string | - |  |

### PublicMessageLocationDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `latitude` | number(double) | - |  |
| `longitude` | number(double) | - |  |
| `address` | string | - |  |
| `name` | string | - |  |
| `url` | string | - |  |

### PublicMessageQuickSendDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `failureReason` | string | - |  |

### PublicMessageTrackDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `type` | enum: `ACCESS_PAGE`, `START_CHAT`, `SAVE_CONTACT` | - |  |
| `pageTitle` | string | - |  |
| `pageUrl` | string | - |  |
| `pageUtm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `isMobileDevice` | boolean | - |  |
| `formData` | [`PublicMessageTrackFromDataDTO`](#publicmessagetrackfromdatadto) | - |  |

### PublicMessageTrackFromDataDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `annotation` | string | - |  |

### PublicMsgTranscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - |  |
| `processing` | boolean | - |  |
| `error` | boolean | - |  |

### PublicQuickMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `sessionId` | string(uuid) | - |  |
| `senderId` | string | - |  |
| `status` | enum: `PROCESSING`, `SAVED`, `QUEUED`, `SENT`, `DELIVERED`, `READ`, `FAILED`, `DELETED`, `WAIT_REPLY` | - |  |
| `statusUrl` | string | - |  |
| `failureReason` | string | - |  |

### PublicQuickSendBodyDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `text` | string | - | Texto da mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `templateId` ou `fileUrl`. |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. Obrigatório caso não seja informado o parâmetro `text` ou `fileUrl`. |
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `fileUrl` | string | - | URL pública de algum arquivo que deseja-se enviar na mensagem. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `fileId` | string(uuid) | - | Código do arquivo que deseja-se enviar na mensagem, o ID pode ser obtido nas rotas /core/v2/file, o arquivo deverá seguir as regras do canal de atendimento. |
| `refId` | string(uuid) | - | ID de referência para identificar a mensagem externamente como resposta a uma mensagem anterior. |

### PublicQuickSendDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | ID da equipe que deverá ser atribuída ao atendimento. Será utilizado somente caso seja criado um novo atendimento. |
| `name` | string | - | Nome da equipe que deverá ser atribuída ao atendimento. Será utilizado somente caso seja criado um novo atendimento. |

### PublicQuickSendOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `enableBot` | boolean | - | Determina se o chatbot deve ser ativado ao receber uma resposta do contato. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. |
| `hiddenSession` | boolean | - | Determina se o atendimento deve estar oculto na tela. Válido apenas caso um novo atendimento seja criado ao enviar a mensagem. O atendimento passará a ser visível caso o contato responda. |
| `forceStartSession` | boolean | - | Se um atendimento estiver em andamento, força o encerramento dele e inicia um novo. |

### PublicQuickSendUserDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | ID do atendente que deverá ser atribuído ao atendimento. Será utilizado somente caso seja criado um novo atendimento. |
| `phoneNumber` | string | - | Telefone do atendente que deverá ser atribuído ao atendimento. Será utilizado somente caso seja criado um novo atendimento. |
| `email` | string | - | Email do atendente que deverá ser atribuído ao atendimento. Será utilizado somente caso seja criado um novo atendimento. |

### PublicReqQuickSendMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `body` | [`PublicQuickSendBodyDTO`](#publicquicksendbodydto) | sim |  |
| `department` | [`PublicQuickSendDepartmentDTO`](#publicquicksenddepartmentdto) | - |  |
| `user` | [`PublicQuickSendUserDTO`](#publicquicksenduserdto) | - |  |
| `options` | [`PublicQuickSendOptionsDTO`](#publicquicksendoptionsdto) | - |  |

### PublicUtmDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sourceId` | string | - |  |
| `source` | string | - |  |
| `clid` | string | - |  |
| `medium` | string | - |  |
| `campaign` | string | - |  |
| `content` | string | - |  |
| `headline` | string | - |  |
| `term` | string | - |  |
| `referralUrl` | string | - |  |


---

# Mensagens Agendadas

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/scheduled-message — Listar

Listagem paginada de mensagens agendadas com filtros opcionais.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `ScheduledAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `ScheduledAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `IncludeDetails` | query | - | enum: `Contact`, `Channel`, `User`, `Department`, `Template`, `Chatbot`[] | Lista de detalhes a serem incluídos na resposta |
| `Status` | query | - | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | Status da mensagem agendada para filtrar |
| `Type` | query | - | enum: `TEMPLATE`, `CHATBOT` | Tipo da mensagem agendada para filtrar |
| `From` | query | - | string | ID ou número de telefone do canal cadastrado na conta. |
| `To` | query | - | string | ID ou número de telefone do destinatário. |
| `User` | query | - | string | ID ou nome do usuário |
| `Department` | query | - | string | ID ou nome da equipe |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicScheduledMessageDTOPublicPageListDTO`](#publicscheduledmessagedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicScheduledMessageDTO`](#publicscheduledmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-scheduled-message

## `POST` /chat/v1/scheduled-message — Criar

Cria uma nova mensagem agendada com os dados fornecidos.

**Body** [`PublicReqCreateScheduledMessageDTO`](#publicreqcreatescheduledmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `department` | [`PublicRequestDepartmentDTO`](#publicrequestdepartmentdto) | - |  |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta (padrão: false) |
| `templateParams` | [`PublicScheduledMessageTemplateParamsDTO`](#publicscheduledmessagetemplateparamsdto) | - |  |

**Resposta 200** [`PublicReqScheduledMessageDTO`](#publicreqscheduledmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-scheduled-message

## `POST` /chat/v1/scheduled-message/batch-cancel — Cancelar em massa

Cancela em massa mensagens agendadas. Apenas mensagens com status agendado podem ser canceladas.

**Body** string(uuid)[]

Array de string(uuid).

**Resposta 200** [`PublicScheduledMessageDTO`](#publicscheduledmessagedto)[]

Array de [`PublicScheduledMessageDTO`](#publicscheduledmessagedto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `sessionId` | string(uuid) | - | Identificador da sessão |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-scheduled-message-batch-cancel

## `GET` /chat/v1/scheduled-message/{id} — Obter por ID

Retorna os detalhes de uma mensagem agendada específica.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem agendada |
| `includeDetails` | query | - | enum: `Contact`, `Channel`, `User`, `Department`, `Template`, `Chatbot`[] | Detalhes adicionais a serem incluídos |

**Resposta 200** [`PublicScheduledMessageDTO`](#publicscheduledmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `sessionId` | string(uuid) | - | Identificador da sessão |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-scheduled-message-id

## `PUT` /chat/v1/scheduled-message/{id} — Atualizar

Atualiza uma mensagem agendada existente. Mensagens já enviadas não podem ser editadas.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem agendada |

**Body** [`PublicReqUpdateScheduledMessageDTO`](#publicrequpdatescheduledmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Undefined`, `To`, `From`, `Department`, `Type`, `TemplateId`, `BotId`, `Scheduling`, `HiddenSession`, `TemplateParams`[] | sim | Campos que devem ser atualizados |
| `to` | string | - | Número de telefone do destinatário. |
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `department` | [`PublicRequestDepartmentDTO`](#publicrequestdepartmentdto) | - |  |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta (padrão: false) |
| `templateParams` | [`PublicScheduledMessageTemplateParamsDTO`](#publicscheduledmessagetemplateparamsdto) | - |  |

**Resposta 200** [`PublicReqScheduledMessageDTO`](#publicreqscheduledmessagedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-scheduled-message-id

## `POST` /chat/v1/scheduled-message/{id}/cancel — Cancelar

Cancela uma mensagem agendada específica. Apenas mensagens com status agendado podem ser canceladas.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da mensagem agendada |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-scheduled-message-id-cancel

---

## Schemas

### PublicFileDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO` | - |  |
| `publicUrl` | string | - |  |
| `publicUrlDownload` | string | - |  |
| `size` | integer(int64) | - |  |
| `isThumbnail` | boolean | - |  |
| `thumbnail` | [`PublicFileThumbnailDTO`](#publicfilethumbnaildto) | - |  |

### PublicFileThumbnailDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `publicUrl` | string | - |  |

### PublicReqCreateScheduledMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `to` | string | sim | Número de telefone do destinatário. |
| `department` | [`PublicRequestDepartmentDTO`](#publicrequestdepartmentdto) | - |  |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta (padrão: false) |
| `templateParams` | [`PublicScheduledMessageTemplateParamsDTO`](#publicscheduledmessagetemplateparamsdto) | - |  |

### PublicReqScheduledMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

### PublicReqUpdateScheduledMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Undefined`, `To`, `From`, `Department`, `Type`, `TemplateId`, `BotId`, `Scheduling`, `HiddenSession`, `TemplateParams`[] | sim | Campos que devem ser atualizados |
| `to` | string | - | Número de telefone do destinatário. |
| `from` | string | - | Número de telefone do canal cadastrado na conta. |
| `department` | [`PublicRequestDepartmentDTO`](#publicrequestdepartmentdto) | - |  |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string | - | ID do modelo de mensagem para a mensagem a ser enviada. |
| `botKey` | string(uuid) | - | Chave do chatbot que será ativado após a resposta do contato. |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta (padrão: false) |
| `templateParams` | [`PublicScheduledMessageTemplateParamsDTO`](#publicscheduledmessagetemplateparamsdto) | - |  |

### PublicRequestDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do departamento |
| `name` | string | - | Nome do departamento (opcional, usado para busca por nome) |

### PublicResponseScheduledMessageTemplateParamsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `file` | [`PublicFileDTO`](#publicfiledto) | - |  |

### PublicScheduledMessageChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do canal |
| `humanId` | string | - | Identificador humano do canal |
| `type` | enum: `GupShup_WhatsApp`, `Dialog360_WhatsApp`, `CloudAPI_WhatsApp`, `ZAPI_WhatsApp`, `EvolutionApi_WhatsApp`, `Instagram`, `Messenger` | - | Tipo do canal (WhatsApp, Instagram, etc.) |

### PublicScheduledMessageChatBotDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Chave única do chatbot |
| `botId` | string(uuid) | - | Id do chatbot |
| `name` | string | - | Nome do chatbot |

### PublicScheduledMessageContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do contato |
| `name` | string | - | Nome do contato |
| `phonenumberFormatted` | string | - | Número de telefone formatado do contato |
| `instagram` | string | - | Usuário do Instagram do contato |
| `pictureUrl` | string | - | URL da foto de perfil do contato |

### PublicScheduledMessageDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único da mensagem agendada |
| `createdAt` | string(date-time) | - | Data e hora de criação da mensagem agendada |
| `updatedAt` | string(date-time) | - | Data e hora da última atualização da mensagem agendada |
| `active` | boolean | - | Indica se a mensagem agendada está ativa |
| `companyId` | string(uuid) | - | Identificador da empresa associada à mensagem agendada |
| `sessionId` | string(uuid) | - | Identificador da sessão |
| `contactId` | string(uuid) | - | Identificador do contato que receberá a mensagem |
| `userId` | string(uuid) | - | Identificador do usuário que criou a mensagem agendada |
| `channelId` | string(uuid) | - | Identificador do canal onde a mensagem será enviada |
| `departmentId` | string(uuid) | - | ID da equipe |
| `status` | enum: `SCHEDULED`, `PROCESSED`, `SENT`, `DELIVERED`, `READ`, `CANCELED`, `FAILED` | - | Status atual da mensagem agendada |
| `type` | enum: `TEMPLATE`, `CHATBOT` | - | Tipo da mensagem agendada |
| `templateId` | string(uuid) | - | Identificador do template utilizado |
| `botId` | string(uuid) | - | Chave do chatbot associado |
| `scheduling` | string(date-time) | - | Data e hora programada para envio da mensagem |
| `hiddenSession` | boolean | - | Indica se a sessão deve ficar oculta |
| `failureReason` | string | - | Indica o motivo de falha caso ocorra |
| `contact` | [`PublicScheduledMessageContactDTO`](#publicscheduledmessagecontactdto) | - |  |
| `user` | [`PublicScheduledMessageUserDTO`](#publicscheduledmessageuserdto) | - |  |
| `channel` | [`PublicScheduledMessageChannelDTO`](#publicscheduledmessagechanneldto) | - |  |
| `department` | [`PublicScheduledMessageDepartmentDTO`](#publicscheduledmessagedepartmentdto) | - |  |
| `chatbot` | [`PublicScheduledMessageChatBotDTO`](#publicscheduledmessagechatbotdto) | - |  |
| `template` | [`PublicScheduledMessageTemplateDTO`](#publicscheduledmessagetemplatedto) | - |  |

### PublicScheduledMessageDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicScheduledMessageDTO`](#publicscheduledmessagedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicScheduledMessageDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do departamento |
| `name` | string | - | Nome do departamento |

### PublicScheduledMessageTemplateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do template |
| `name` | string | - | Nome do template |
| `templateParams` | [`PublicResponseScheduledMessageTemplateParamsDTO`](#publicresponsescheduledmessagetemplateparamsdto) | - |  |

### PublicScheduledMessageTemplateParamsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `parameters` | object | - | Parâmetros do modelo de mensagem. Obrigatório caso o modelo de mensagem informado no `templateId` possua parâmetros. |
| `fileUrl` | string | - | URL pública de algum arquivo que deseja-se enviar na mensagem. O arquivo enviado deverá seguir as regras do canal de atendimento. |
| `fileId` | string(uuid) | - | Código do arquivo que deseja-se enviar na mensagem, o ID pode ser obtido nas rotas /core/v2/file, o arquivo deverá seguir as regras do canal de atendimento. |

### PublicScheduledMessageUserDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - | Identificador único do usuário |
| `name` | string | - | Nome do usuário |


---

# Modelos de Mensagem

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/template — Listar

Listagem paginada de modelos de mensagem.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Archived` | query | - | boolean | Filtro por modelos de mensagem arquivados. |
| `Name` | query | - | string | Filtro por nome do modelo de mensagem. |
| `SearchableText` | query | - | string | Filtro por conteúdo do modelo de mensagem. |
| `ChannelId` | query | - | string(uuid) | Filtro por id do canal. |
| `ApprovedOnly` | query | - | boolean | Filtro por status do modelo de mensagem. |
| `Type` | query | - | enum: `QUICKREPLY`, `ATTENDANCE`, `CAMPAIGN`, `SEQUENCE`, `SCHEDULEDMESSAGE`, `AUTHENTICATION` | Filtro por tipo do modelo de mensagem. |
| `IncludeDetails` | query | - | enum: `All`, `Params`, `File`, `Interactive`[] | Detalhes que devem ser incluidos na resposta. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicTemplateDTOPublicPageListDTO`](#publictemplatedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicTemplateDTO`](#publictemplatedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-template

---

## Schemas

### PublicTemplateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `archived` | boolean | - |  |
| `channelId` | string(uuid) | - |  |
| `name` | string | - |  |
| `text` | string | - |  |
| `footerText` | string | - |  |
| `status` | enum: `Draft`, `Approved`, `Disapproved`, `InRevision`, `Paused`, `Disabled`, `Deleted` | - |  |
| `channelType` | enum: `GUPSHUP_WHATSAPP`, `DIALOG360_WHATSAPP`, `CLOUDAPI_WHATSAPP`, `ZAPI_WHATSAPP`, `EVOLUTIONAPI_WHATSAPP`, `INSTAGRAM`, `MESSENGER` | - |  |
| `type` | enum: `UNDEFINED`, `QUICKREPLY`, `TEMPLATE`, `TEMPLATE_CAMPAIGN`, `TEMPLATE_SEQUENCE`, `SYSTEM`, `TEMPLATE_SCHEDULED_MESSAGE`, `AUTHENTICATION`[] | - |  |
| `params` | [`PublicTemplateParamDTO`](#publictemplateparamdto)[] | - |  |
| `internalName` | string | - |  |
| `fileType` | enum: `UNDEFINED`, `IMAGE`, `VIDEO`, `DOCUMENT` | - |  |
| `quickReplyAlias` | string | - |  |
| `rejectedDescription` | string | - |  |
| `categoryId` | string(uuid) | - |  |
| `categoryName` | string | - |  |

### PublicTemplateDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicTemplateDTO`](#publictemplatedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicTemplateParamDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - |  |
| `templateId` | string(uuid) | - |  |


---

# Painéis

Serviço `crm` — base `https://api.wts.chat/crm`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /crm/v1/panel/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do painel. |
| `IncludeDetails` | query | - | enum: `Tags`, `Steps`, `StepsFields`, `StepsCardCount`, `Cards`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicPanelDTO`](#publicpaneldto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `archived` | boolean | - |  |
| `scope` | enum: `COMPANY`, `DEPARTMENT`, `USER` | - |  |
| `departmentIds` | string(uuid)[] | - |  |
| `userId` | string(uuid) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `thumbnailId` | string(uuid) | - |  |
| `thumbnailFile` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `key` | string | - |  |
| `overdueCardCount` | integer(int32) | - |  |
| `stepTitles` | string[] | - |  |
| `tags` | [`PublicPanelTagDTO`](#publicpaneltagdto)[] | - |  |
| `steps` | [`PublicPanelStepDTO`](#publicpanelstepdto)[] | - |  |
| `type` | enum: `MANAGEMENT`, `SALES` | - |  |
| `autoLossDays` | integer(int32) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-panel-id

## `GET` /crm/v1/panel/{id}/custom-fields — Campos personalizados

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do painel. |
| `NestedList` | query | - | boolean | Determina a estrutura da lista retornada. Se verdadeiro, os campos serão retornados de forma aninhada, isto é, estruturado em grupos. |

**Resposta 200** [`PublicCustomFieldDTO`](#publiccustomfielddto)[]

Array de [`PublicCustomFieldDTO`](#publiccustomfielddto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-panel-id-custom-fields

## `GET` /crm/v1/panel/{id}/lost-reason — Listar motivos de perda

Listagem paginada de motivos de perda do painel.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do painel do tipo Vendas. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicPanelCardResultDTOPublicPageListDTO`](#publicpanelcardresultdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardResultDTO`](#publicpanelcardresultdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-panel-id-lost-reason

## `GET` /crm/v2/panel — Listar painéis

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `Title` | query | - | string | Filtro por título do painel. |
| `Type` | query | - | enum: `MANAGEMENT`, `SALES` | Filtro por tipo do painel. |
| `IncludeDetails` | query | - | enum: `Tags`, `Steps`, `StepsCardCount`, `PanelCardOverdueCount`[] | Detalhes que devem ser incluídos na resposta. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicPanelDTOPublicPageListDTO`](#publicpaneldtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelDTO`](#publicpaneldto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-panel

---

## Schemas

### PublicCustomFieldDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `parentId` | string(uuid) | - |  |
| `type` | enum: `GROUP`, `STRING`, `TEXT`, `INTEGER`, `FLOAT`, `SINGLESELECT`, `MULTISELECT`, `DATE`, `TIME`, `DATETIME`, `BOOLEAN` | - |  |
| `entityType` | enum: `CONTACT`, `PANEL` | - |  |
| `scopeId` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `key` | string | - |  |
| `position` | integer(int32) | - |  |
| `required` | boolean | - |  |
| `visible` | boolean | - |  |
| `isValueRange` | boolean | - |  |
| `options` | [`PublicCustomFieldOptionDTO`](#publiccustomfieldoptiondto)[] | - |  |
| `children` | [`PublicCustomFieldDTO`](#publiccustomfielddto)[] | - |  |

### PublicCustomFieldOptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicFileDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `extension` | string | - |  |
| `mimeType` | string | - |  |
| `type` | enum: `UNDEFINED`, `PDF`, `EXCEL`, `WORD`, `IMAGE`, `AUDIO`, `VIDEO` | - |  |
| `publicUrl` | string | - |  |
| `publicUrlDownload` | string | - |  |
| `size` | integer(int64) | - |  |
| `isThumbnail` | boolean | - |  |
| `thumbnail` | [`PublicFileThumbnailDTO`](#publicfilethumbnaildto) | - |  |

### PublicFileThumbnailDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `publicUrl` | string | - |  |

### PublicPanelCardContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicPanelCardDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `panelTitle` | string | - |  |
| `stepId` | string(uuid) | - |  |
| `stepTitle` | string | - |  |
| `stepPhase` | enum: `NONE`, `INITIAL`, `FINAL` | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `key` | string | - |  |
| `number` | integer(int32) | - |  |
| `dueDate` | string(date-time) | - |  |
| `isOverdue` | boolean | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `sessionId` | string(uuid) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `responsibleUserId` | string(uuid) | - |  |
| `responsibleUser` | [`PublicPanelCardResponsibleUserDTO`](#publicpanelcardresponsibleuserdto) | - |  |
| `contactIds` | string(uuid)[] | - |  |
| `contacts` | [`PublicPanelCardContactDTO`](#publicpanelcardcontactdto)[] | - |  |
| `customFields` | object | - |  |
| `metadata` | object | - |  |
| `archived` | boolean | - |  |

### PublicPanelCardDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardDTO`](#publicpanelcarddto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPanelCardResponsibleUserDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |

### PublicPanelCardResultDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `description` | string | - |  |

### PublicPanelCardResultDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelCardResultDTO`](#publicpanelcardresultdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPanelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `archived` | boolean | - |  |
| `scope` | enum: `COMPANY`, `DEPARTMENT`, `USER` | - |  |
| `departmentIds` | string(uuid)[] | - |  |
| `userId` | string(uuid) | - |  |
| `title` | string | - |  |
| `description` | string | - |  |
| `thumbnailId` | string(uuid) | - |  |
| `thumbnailFile` | [`PublicFileDTO`](#publicfiledto) | - |  |
| `key` | string | - |  |
| `overdueCardCount` | integer(int32) | - |  |
| `stepTitles` | string[] | - |  |
| `tags` | [`PublicPanelTagDTO`](#publicpaneltagdto)[] | - |  |
| `steps` | [`PublicPanelStepDTO`](#publicpanelstepdto)[] | - |  |
| `type` | enum: `MANAGEMENT`, `SALES` | - |  |
| `autoLossDays` | integer(int32) | - |  |

### PublicPanelDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicPanelDTO`](#publicpaneldto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicPanelStepDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `archived` | boolean | - |  |
| `position` | number(double) | - |  |
| `title` | string | - |  |
| `isInitial` | boolean | - |  |
| `isFinal` | boolean | - |  |
| `cardCount` | integer(int32) | - |  |
| `overdueCardCount` | integer(int32) | - |  |
| `monetaryAmount` | number(double) | - |  |
| `fields` | [`PublicPanelStepFieldDTO`](#publicpanelstepfielddto)[] | - |  |
| `cards` | [`PublicPanelCardDTOPublicPageListDTO`](#publicpanelcarddtopublicpagelistdto) | - |  |

### PublicPanelStepFieldDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `key` | string | - |  |
| `type` | enum: `DEFAULT_FIELD`, `CUSTOM_FIELD` | - |  |
| `position` | integer(int32) | - |  |
| `visible` | boolean | - |  |

### PublicPanelTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `panelId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameColor` | string | - |  |
| `bgColor` | string | - |  |


---

# Sequências

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/sequence — Listar

Listagem paginada de sequências.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `IncludeDetails` | query | - | enum: `ContactExecutingCount`, `ExecutionStats`[] |  |
| `Name` | query | - | string |  |
| `ContactId` | query | - | string(uuid) |  |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicSequenceDTOPublicPageListDTO`](#publicsequencedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceDTO`](#publicsequencedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-sequence

## `DELETE` /chat/v1/sequence/{id}/contact — Remover contato

Remova um contato de uma sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceContactDTO`](#publicrequestsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-sequence-id-contact

## `POST` /chat/v1/sequence/{id}/contact — Adicionar contato

Adicione um contato em uma sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceContactDTO`](#publicrequestsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

**Resposta 200** [`PublicSequenceContactDTO`](#publicsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sequenceId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactName` | string | - |  |
| `origin` | enum: `USER_SINGLE`, `USER_FILTER`, `CHATBOT`, `API` | - |  |
| `addedByUserId` | string(uuid) | - |  |
| `addedByChatbotId` | string(uuid) | - |  |
| `lastAddedAt` | string(date-time) | - |  |
| `contactDetails` | [`PublicSequenceContactDetailsDTO`](#publicsequencecontactdetailsdto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-sequence-id-contact

## `DELETE` /chat/v1/sequence/{id}/contact/batch — Remover contatos

Remova contatos de uma sequência adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceBatchContactDTO`](#publicrequestsequencebatchcontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-sequence-id-contact-batch

## `POST` /chat/v1/sequence/{id}/contact/batch — Adicionar contatos

Adicione contatos em uma sequência adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceBatchContactDTO`](#publicrequestsequencebatchcontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

**Resposta 200** [`PublicSequenceContactDTOPublicPageListDTO`](#publicsequencecontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-sequence-id-contact-batch

## `GET` /chat/v2/sequence/{id}/contact — Listar contatos

Listagem paginada de contatos da sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |
| `IncludeDetails` | query | - | enum: `ContactDetails`[] |  |
| `Name` | query | - | string | Nome do contato. |
| `ContactId` | query | - | string(uuid) | Id do contato. |
| `PhoneNumber` | query | - | string | Número do contato. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicSequenceContactDTOPublicPageListDTO`](#publicsequencecontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-sequence-id-contact

---

## Schemas

### PublicRequestSequenceBatchContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

### PublicRequestSequenceContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

### PublicSequenceContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sequenceId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactName` | string | - |  |
| `origin` | enum: `USER_SINGLE`, `USER_FILTER`, `CHATBOT`, `API` | - |  |
| `addedByUserId` | string(uuid) | - |  |
| `addedByChatbotId` | string(uuid) | - |  |
| `lastAddedAt` | string(date-time) | - |  |
| `contactDetails` | [`PublicSequenceContactDetailsDTO`](#publicsequencecontactdetailsdto) | - |  |

### PublicSequenceContactDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicSequenceContactDetailsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |
| `phonenumber` | string | - |  |
| `phonenumberFormatted` | string | - |  |
| `instagram` | string | - |  |
| `email` | string | - |  |
| `pictureUrl` | string | - |  |

### PublicSequenceDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `enabled` | boolean | - |  |
| `contactExecutingCount` | integer(int32) | - |  |

### PublicSequenceDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceDTO`](#publicsequencedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |


---

# Usuários

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/agent — Listar

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)[]

Array de [`PublicAgentDTO`](#publicagentdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-agent

## `POST` /core/v1/agent — Criar

**Body** [`PublicAgentCreateDTO`](#publicagentcreatedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome do usuário |
| `email` | string(email) | - | Email do usuário |
| `phoneNumber` | string | - | Telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | sim | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent

## `DELETE` /core/v1/agent/{id} — Excluir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`RequestAgentDepartmentDeleteDTO`](#requestagentdepartmentdeletedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionResolution` | enum: `COMPLETE`, `TRANSFER`, `RETURN_TO_PENDING` | - |  |
| `transferUserId` | string(uuid) | - | ID do usuário que receberá os atendimentos em andamento. Obrigatório quando o campo sessionResolution for igual a TRANSFER |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-agent-id

## `GET` /core/v1/agent/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-agent-id

## `PUT` /core/v1/agent/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentUpdatePartialDTO`](#publicagentupdatepartialdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do usuário |
| `shortName` | string | - | Nome curto/apelido do usuário |
| `email` | string | - | Email do usuário |
| `phoneNumber` | string | - | Número de telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | - | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |
| `fields` | enum: `Undefined`, `Name`, `ShortName`, `PhoneNumber`, `Email`, `Profile`, `Availability`[] | sim | Campos que devem ser atualizados |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-agent-id

## `POST` /core/v1/agent/{id}/departments — Atualizar equipes

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentDepartmentUpdateDTO`](#publicagentdepartmentupdatedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim | Ação a ser executada: REPLACE_ALL, UPSERT ou REMOVE |
| `items` | [`PublicAgentDepartmentItemDTO`](#publicagentdepartmentitemdto)[] | sim | Lista de equipes para atualização |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-departments

## `POST` /core/v1/agent/{id}/logout — Fazer logout

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-logout

## `POST` /core/v1/agent/{id}/status — Alterar status

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentChangeStatusDTO`](#publicagentchangestatusdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `status` | enum: `Undefined`, `Active`, `Blocked` | sim | Novo status do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-status

---

## Schemas

### PublicAgentChangeStatusDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `status` | enum: `Undefined`, `Active`, `Blocked` | sim | Novo status do usuário |

### PublicAgentCreateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome do usuário |
| `email` | string(email) | - | Email do usuário |
| `phoneNumber` | string | - | Telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | sim | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |

### PublicAgentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

### PublicAgentDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `agentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicAgentDepartmentItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `departmentId` | string | sim | ID da equipe |
| `isAgent` | boolean | - | Se é usuário na equipe |
| `isSupervisor` | boolean | - | Se é supervisor na equipe |

### PublicAgentDepartmentUpdateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim | Ação a ser executada: REPLACE_ALL, UPSERT ou REMOVE |
| `items` | [`PublicAgentDepartmentItemDTO`](#publicagentdepartmentitemdto)[] | sim | Lista de equipes para atualização |

### PublicAgentUpdatePartialDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do usuário |
| `shortName` | string | - | Nome curto/apelido do usuário |
| `email` | string | - | Email do usuário |
| `phoneNumber` | string | - | Número de telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | - | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |
| `fields` | enum: `Undefined`, `Name`, `ShortName`, `PhoneNumber`, `Email`, `Profile`, `Availability`[] | sim | Campos que devem ser atualizados |

### RequestAgentDepartmentDeleteDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionResolution` | enum: `COMPLETE`, `TRANSFER`, `RETURN_TO_PENDING` | - |  |
| `transferUserId` | string(uuid) | - | ID do usuário que receberá os atendimentos em andamento. Obrigatório quando o campo sessionResolution for igual a TRANSFER |


---

# Webhooks

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/webhook/event — Listar eventos

Listagem dos eventos de webhook que podem ser assinados.

**Resposta 200** [`PublicWebhookEventDTO`](#publicwebhookeventdto)[]

Array de [`PublicWebhookEventDTO`](#publicwebhookeventdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `event` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4) | - |  |
| `description` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-event

## `GET` /core/v1/webhook/subscription — Listar assinaturas

Listagem das assinaturas de webhook ativas e inativas.

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)[]

Array de [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-subscription

## `POST` /core/v1/webhook/subscription — Cria assinatura

Cria assinatura de webhook.

**Body** [`PublicReqCreateWebhookSubscriptionDTO`](#publicreqcreatewebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome para identificação da assinatura |
| `url` | string | sim | URL destino para onde serão enviadas requisições POST |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa) |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | sim | Eventos que deverão ser enviados para esta assinatura |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-webhook-subscription

## `DELETE` /core/v1/webhook/subscription/{subscriptionId} — Remove assinatura

Remove assinatura de webhook.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-webhook-subscription-subscriptionid

## `GET` /core/v1/webhook/subscription/{subscriptionId} — Busca assinatura por ID

Busca assinatura de webhook através do ID.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-subscription-subscriptionid

## `PUT` /core/v1/webhook/subscription/{subscriptionId} — Atualiza assinatura

Atualiza assinatura de webhook.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Body** [`PublicReqUpdateWebhookSubscriptionDTO`](#publicrequpdatewebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `Url`, `Events`, `Enabled`[] | sim | Campos a serem atualizados. |
| `name` | string | - | Nome para identificação da assinatura. |
| `url` | string | - | URL destino para onde serão enviadas requisições POST. |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa). |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | - | Tópicos de webhook que deverão ser inscritos nesta assinatura. |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-webhook-subscription-subscriptionid

---

## Schemas

### PublicReqCreateWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome para identificação da assinatura |
| `url` | string | sim | URL destino para onde serão enviadas requisições POST |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa) |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | sim | Eventos que deverão ser enviados para esta assinatura |

### PublicReqUpdateWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `Url`, `Events`, `Enabled`[] | sim | Campos a serem atualizados. |
| `name` | string | - | Nome para identificação da assinatura. |
| `url` | string | - | URL destino para onde serão enviadas requisições POST. |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa). |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | - | Tópicos de webhook que deverão ser inscritos nesta assinatura. |

### PublicWebhookEventDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `event` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4) | - |  |
| `description` | string | - |  |

### PublicWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |


---
