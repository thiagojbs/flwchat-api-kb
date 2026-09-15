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
