# Sequências

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/sequence — Listar

Listagem paginada de sequências.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `IncludeDetails` | query | - | enum: `ContactExecutingCount`, `ExecutionStats`[] |  |
| `Name` | query | - | string |  |
| `ContactId` | query | - | string(uuid) |  |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicSequenceDTOPublicPageListDTO`](#publicsequencedtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceDTO`](#publicsequencedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-sequence

## `DELETE` /chat/v1/sequence/{id}/contact — Remover contato

Remova um contato de uma sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceContactDTO`](#publicrequestsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-sequence-id-contact

## `POST` /chat/v1/sequence/{id}/contact — Adicionar contato

Adicione um contato em uma sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceContactDTO`](#publicrequestsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

**Resposta 200** [`PublicSequenceContactDTO`](#publicsequencecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sequenceId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactName` | string | - |  |
| `origin` | enum: `USER_SINGLE`, `USER_FILTER`, `CHATBOT`, `API` | - |  |
| `addedByUserId` | string(uuid) | - |  |
| `addedByChatbotId` | string(uuid) | - |  |
| `lastAddedAt` | string(date-time) | - |  |
| `contactDetails` | [`PublicSequenceContactDetailsDTO`](#publicsequencecontactdetailsdto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-sequence-id-contact

## `DELETE` /chat/v1/sequence/{id}/contact/batch — Remover contatos

Remova contatos de uma sequência adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceBatchContactDTO`](#publicrequestsequencebatchcontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-sequence-id-contact-batch

## `POST` /chat/v1/sequence/{id}/contact/batch — Adicionar contatos

Adicione contatos em uma sequência adicionando um filtro.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |

**Body** [`PublicRequestSequenceBatchContactDTO`](#publicrequestsequencebatchcontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

**Resposta 200** [`PublicSequenceContactDTOPublicPageListDTO`](#publicsequencecontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-sequence-id-contact-batch

## `GET` /chat/v2/sequence/{id}/contact — Listar contatos

Listagem paginada de contatos da sequência.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da sequência. |
| `IncludeDetails` | query | - | enum: `ContactDetails`[] |  |
| `Name` | query | - | string | Nome do contato. |
| `ContactId` | query | - | string(uuid) | Id do contato. |
| `PhoneNumber` | query | - | string | Número do contato. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicSequenceContactDTOPublicPageListDTO`](#publicsequencecontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-sequence-id-contact

---

## Schemas

### PublicRequestSequenceBatchContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactIds` | string(uuid)[] | - | Filtro por ids. |
| `phoneNumbers` | string[] | - | Filtro por números de telefones. Caso o contato não exista ele será criado |

### PublicRequestSequenceContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `contactId` | string(uuid) | - | ID do contato. |
| `phoneNumber` | string | - | Telefone do contato. |

### PublicSequenceContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `sequenceId` | string(uuid) | - |  |
| `contactId` | string(uuid) | - |  |
| `contactName` | string | - |  |
| `origin` | enum: `USER_SINGLE`, `USER_FILTER`, `CHATBOT`, `API` | - |  |
| `addedByUserId` | string(uuid) | - |  |
| `addedByChatbotId` | string(uuid) | - |  |
| `lastAddedAt` | string(date-time) | - |  |
| `contactDetails` | [`PublicSequenceContactDetailsDTO`](#publicsequencecontactdetailsdto) | - |  |

### PublicSequenceContactDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceContactDTO`](#publicsequencecontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

### PublicSequenceContactDetailsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `name` | string | - |  |
| `phonenumber` | string | - |  |
| `phonenumberFormatted` | string | - |  |
| `instagram` | string | - |  |
| `email` | string | - |  |
| `pictureUrl` | string | - |  |

### PublicSequenceDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `active` | boolean | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `enabled` | boolean | - |  |
| `contactExecutingCount` | integer(int32) | - |  |

### PublicSequenceDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicSequenceDTO`](#publicsequencedto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |
