# API flw.chat — bloco para colar no chat

Abra o Claude ou o ChatGPT, copie TUDO que está entre as linhas marcadas e cole na conversa.
A partir daí, é só pedir em português: "escreve o código que envia um template pelo flw.chat".

Vale para aquela conversa. Em conversa nova, cole de novo.

==================== COPIE DAQUI ====================

Você vai trabalhar com a API do flw.chat (plataforma de atendimento em WhatsApp, Instagram e
Messenger). Use SOMENTE as informações abaixo — não deduza URLs nem campos.

BASE URL
https://api.wts.chat/{serviço}/{versão}/{recurso}
O prefixo de serviço é obrigatório. São três:
  core -> contatos, etiquetas, campos personalizados, usuários, equipes, carteiras, arquivos, webhooks
  chat -> conversas, mensagens, envios, templates, chatbots, canais, sequências, agendamentos
  crm  -> painéis (funis), cards, anotações
Exemplo correto: https://api.wts.chat/chat/v1/send/template
ERRADO: https://api.flw.chat/v1/send/template (sem prefixo devolve 400 badrequest).

AUTENTICAÇÃO
Header em toda requisição: Authorization: Bearer pn_SEU_TOKEN
Token gerado na plataforma em Ajustes > Integrações > Integração via API.
Token inválido devolve 401 com key ERROR_UNAUTHORIZED. Rota inexistente sem token também devolve 401.

RATE LIMIT (dois limites independentes)
Geral: 1000 requisições / 5 min por conta, com burst de 200 / 5 s.
Endpoints /chat/v1/send/*: 1000 requisições / 2 min próprios.
Estourou: 429. Use backoff, nunca repita na hora.

PAGINAÇÃO
Parâmetros pageNumber e pageSize (máximo 100). Resposta:
{"pageNumber":1,"pageSize":50,"totalPages":5,"totalItems":250,"hasMorePages":true,"items":[...]}
Itere enquanto hasMorePages for true e mantenha pageSize constante.

ERRO (todos os 4xx e 5xx)
{"id":{"value":"uuid","shortValue":"c44bf0cc"},"httpStatusCode":401,"error":true,
 "date":"2026-09-15T19:41:56Z","key":"ERROR_UNAUTHORIZED","text":"Acesso negado",
 "isUnsolvableError":false}
Guarde id.shortValue para abrir chamado no suporte.

FORMATOS
Telefone: "+55|11999999999" (DDI, pipe, número sem máscara).
Campo "to": telefone ou @usuarioinstagram do destinatário.
Campo "from": número ou @usuario do canal da conta (liste em GET /chat/v1/channel).
IDs são UUID. Datas em ISO-8601 UTC.

ENVIAR MENSAGEM
Use POST /chat/v1/send/{text|image|audio|video|document|template|otp|typing|chatbot}.
Variantes: /chat/v1/send/template/batch e /chat/v1/send/chatbot/batch (até 100 por requisição).
Dentro de uma conversa que você já tem o ID: POST /chat/v1/session/{id}/message.
Precisa do status na mesma chamada: POST /chat/v1/message/send-sync (espera até 25 s).

REGRAS DE ENVIO
1. No WhatsApp, conversa só pode ser INICIADA com template. Sem conversa aberta, send/text é
   recusado. Use send/template com templateId vindo de GET /chat/v1/template e parameters preenchido.
   Texto livre só depois que o contato responde.
2. Contato que não existe é criado automaticamente no envio.
3. Envio é assíncrono: a resposta traz id e status inicial, não a entrega. Acompanhe em
   GET /chat/v1/send/message/{id} ou passe callbackUrl no corpo para receber webhook.
4. Status de mensagem: PROCESSING, SAVED, QUEUED, SENT, DELIVERED, READ, FAILED, DELETED, WAIT_REPLY.
   Status de OTP é outro conjunto: UNDEFINED, PENDING, SENT, RECEIVED, FAILED.
5. options controla o atendimento criado: enableBot, hiddenSession, forceStartSession, user, department.
6. senderId é um ID seu, opcional, para rastrear a mensagem depois sem guardar o ID da plataforma.

EXEMPLO — enviar template
curl -X POST https://api.wts.chat/chat/v1/send/template \
  -H "Authorization: Bearer $FLW_TOKEN" -H "Content-Type: application/json" \
  -d '{"to":"+55|11999999999","templateId":"UUID_DO_TEMPLATE",
       "parameters":{"1":"João","2":"12345"},"senderId":"pedido-9876",
       "options":{"enableBot":true}}'

ENVIAR ARQUIVO
O campo fileIdOrUrl aceita URL pública (mais simples) ou um FileId da plataforma. Para o FileId:
1) GET https://api.wts.chat/core/v2/file?Type=IMAGE&Name=foto.jpg&MimeType=image/jpeg
   devolve {"tempFileId":"...","urlUpload":"..."}
2) PUT do conteúdo do arquivo na urlUpload (sem header Authorization)
3) POST https://api.wts.chat/core/v2/file com {"tempFileId":"..."} devolve o id definitivo
Type aceita UNDEFINED, PDF, EXCEL, WORD, IMAGE, AUDIO, VIDEO, DOCUMENT. O FileId é reutilizável.

WEBHOOKS
Assine em POST /core/v1/webhook/subscription ou na plataforma. Você recebe POST com:
{"eventType":"CONTACT_UPDATE","date":"2026-09-15T16:42:35Z","content":{...}}
Eventos: SESSION_NEW, SESSION_UPDATE, SESSION_COMPLETE, MESSAGE_RECEIVED, MESSAGE_UPDATED,
MESSAGE_SENT, CONTACT_NEW, CONTACT_UPDATE, CONTACT_TAG_UPDATE, PAYMENT_NEW, PAYMENT_UPDATE,
PANEL_CARD_NEW, PANEL_CARD_UPDATE, PANEL_CARD_STEP_CHANGE, PANEL_CARD_NOTE_NEW,
PANEL_CARD_NOTE_UPDATE.

PRINCIPAIS ROTAS (109 no total)
core: GET/POST /core/v1/contact · POST /core/v1/contact/filter · GET|PUT /core/v1/contact/{id}
      POST /core/v2/contact/batch (até 100) · GET /core/v1/contact/phonenumber/{phone}
      POST /core/v1/contact/{id}/tags · GET/POST /core/v1/tag · GET /core/v1/custom-field
      GET/POST /core/v1/agent · GET/POST /core/v1/department · GET /core/v1/portfolio
      GET/POST /core/v1/webhook/subscription · GET /core/v1/webhook/event · GET/POST /core/v2/file
chat: GET /chat/v2/session · GET /chat/v2/session/{id} · PUT /chat/v1/session/{id}/transfer
      PUT /chat/v1/session/{id}/assignee · PUT /chat/v1/session/{id}/complete
      PUT /chat/v2/session/{id}/partial · GET/POST /chat/v1/session/{id}/note
      GET /chat/v1/session/{id}/message · POST /chat/v1/send/* · GET /chat/v1/message/{id}/status
      GET /chat/v1/template · GET /chat/v1/channel · GET /chat/v1/chatbot
      GET/POST /chat/v1/scheduled-message · GET /chat/v1/sequence
crm:  GET/POST /crm/v2/panel/card · GET /crm/v2/panel/card/{id} · PUT /crm/v3/panel/card/{id}
      POST /crm/v2/panel/card/{id}/duplicate · GET /crm/v2/panel · GET /crm/v1/panel/{id}

DOCUMENTAÇÃO COMPLETA
Se você conseguir acessar a internet, busque o detalhe de campos em:
https://raw.githubusercontent.com/thiagojbs/flwchat-api-kb/main/SKILL.md
Referência de todos os endpoints, campo a campo:
https://github.com/thiagojbs/flwchat-api-kb/tree/main/reference

Quando eu pedir algo dessa API: confirme a rota completa com prefixo de serviço, monte o payload só
com campos que existem e trate 429 com backoff. Se faltar informação, diga o que falta em vez de
inventar campo.

==================== ATÉ AQUI ====================

Quem usa Claude Code ou Codex no terminal não precisa colar nada a cada conversa — instale de uma vez:
https://github.com/thiagojbs/flwchat-api-kb/blob/main/INSTALL.md

Seu token é pessoal (Ajustes > Integrações > Integração via API). Não cole o token no chat.
