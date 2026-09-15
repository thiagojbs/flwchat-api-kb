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
