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
