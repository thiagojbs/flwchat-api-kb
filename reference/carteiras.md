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
