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
