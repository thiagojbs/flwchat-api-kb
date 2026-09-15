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
