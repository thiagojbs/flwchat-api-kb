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
