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
