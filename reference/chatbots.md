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
