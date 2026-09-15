# Contatos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/contact — Listar

Listagem paginada de contatos. Para resultados mais específicos, utilize o endpoint `/filter`.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |
| `Status` | query | - | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `CreatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `CreatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.Before` | query | - | string(date-time) | Limite superior de busca, sempre em fuso horário UTM. |
| `UpdatedAt.After` | query | - | string(date-time) | Limite inferior de busca, sempre em fuso horário UTM. |
| `PageNumber` | query | - | integer(int32) | Número da página a ser obtida. |
| `PageSize` | query | - | integer(int32) | Tamanho da página a ser obtida. |
| `OrderBy` | query | - | string | Nome do campo para ser utilizado como pivô da ordenação. |
| `OrderDirection` | query | - | enum: `ASCENDING`, `DESCENDING` | Determina se a ordenação deve ser crescente ou decrescente. |

**Resposta 200** [`PublicContactDTOPublicPageListDTO`](#publiccontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact

## `POST` /core/v1/contact — Criar

**Body** [`PublicReqCreateContactIndividualDTO`](#publicreqcreatecontactindividualdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact

## `GET` /core/v1/contact/custom-field — Campos personalizados

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
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
Doc: https://flwchat.readme.io/reference/get_v1-contact-custom-field

## `POST` /core/v1/contact/filter — Filtrar

Filtragem paginada de contatos.

**Body** [`PublicReqFilterContactDTO`](#publicreqfiltercontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `createdAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `updatedAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `includeDetails` | enum: `Tags`, `CustomFields`, `Portfolios`[] | - | Detalhes que devem ser incluídos na resposta. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `textFilter` | string | - | Filtro textual. A busca é realizada nos atributos textuais relevantes do contato. |
| `name` | string | - | Filtro por nome. |
| `phoneNumber` | string | - | Filtro por número de telefone. |
| `email` | string | - | Filtro por email. |
| `instagram` | string | - | Filtro por nome de usuário do Instagram. |
| `tagIds` | string(uuid)[] | - | Filtro por etiquetas usando IDs. |
| `tagNames` | string[] | - | Filtro por etiquetas usando nomes. |
| `portfolioIds` | string(uuid)[] | - | Filtro por carteiras usando IDs. |
| `portfolioNames` | string[] | - | Filtro por carteiras usando nomes. |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - | Filtro por origem. |
| `customFields` | object | - | Filtro por valores de campos personalizados. |
| `metadata` | object | - | Filtro por metadados. |

**Resposta 200** [`PublicContactDTOPublicPageListDTO`](#publiccontactdtopublicpagelistdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-filter

## `GET` /core/v1/contact/phonenumber/{phone} — Obter por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone |
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact-phonenumber-phone

## `PUT` /core/v1/contact/phonenumber/{phone} — Atualizar por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone. |

**Body** [`PublicReqUpdateContactDTO`](#publicrequpdatecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-contact-phonenumber-phone

## `POST` /core/v1/contact/phonenumber/{phone}/tags — Atualizar etiquetas por Número de telefone

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `phone` | path | sim | string | Número de telefone |

**Body** [`PublicReqUpdateContactTagDTO`](#publicrequpdatecontacttagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-phonenumber-phone-tags

## `GET` /core/v1/contact/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato |
| `IncludeDetails` | query | - | enum: `Tags`, `CustomFields`, `Portfolios`[] | Detalhes que devem ser incluídos na resposta. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-contact-id

## `POST` /core/v1/contact/{id}/tags — Atualizar etiquetas

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato ou número de telefone. |

**Body** [`PublicReqUpdateContactTagDTO`](#publicrequpdatecontacttagdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-contact-id-tags

## `POST` /core/v2/contact/batch — Salvar em massa

Permite salvar até 100 contatos em uma única requisição. Se um contato com o mesmo número de telefone, Instagram ou endereço de email já existir, este apenas será atualizado.

**Body** [`PublicReqBatchCreateContactV2DTO`](#publicreqbatchcreatecontactv2dto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `items` | [`PublicReqCreateContactDTO`](#publicreqcreatecontactdto)[] | sim | Dados para criação dos contatos. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)[]

Array de [`PublicContactDTO`](#publiccontactdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v2-contact-batch

## `PUT` /core/v2/contact/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do contato. |

**Body** [`PublicReqUpdateContactDTO`](#publicrequpdatecontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

**Resposta 200** [`PublicContactDTO`](#publiccontactdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v2-contact-id

---

## Schemas

### PublicContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `nameWhatsapp` | string | - |  |
| `nameInstagram` | string | - |  |
| `nameMessenger` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `email` | string | - |  |
| `instagram` | string | - |  |
| `messengerId` | string | - |  |
| `annotation` | string | - |  |
| `tagIds` | string(uuid)[] | - |  |
| `tagNames` | string[] | - |  |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - |  |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - |  |
| `importedAt` | string(date-time) | - |  |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `customFields` | object | - |  |
| `portfolioIds` | string(uuid)[] | - |  |
| `portfolioNames` | string[] | - |  |
| `metadata` | object | - |  |

### PublicContactDTOPublicPageListDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `items` | [`PublicContactDTO`](#publiccontactdto)[] | - |  |
| `totalItems` | integer(int32) | - |  |
| `totalPages` | integer(int32) | - |  |
| `hasMorePages` | boolean | - |  |

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

### PublicDateFilterDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `before` | string(date-time) | - | Limite superior de busca, sempre em fuso horário UTM. |
| `after` | string(date-time) | - | Limite inferior de busca, sempre em fuso horário UTM. |

### PublicReqBatchCreateContactV2DTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `items` | [`PublicReqCreateContactDTO`](#publicreqcreatecontactdto)[] | sim | Dados para criação dos contatos. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

### PublicReqContactUpdatePartialOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagsOperation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Define como as listas de tags devem ser tratadas ao atualizar, como padrão será InsertIfNotExists |

### PublicReqCreateContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |

### PublicReqCreateContactIndividualDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `options` | [`PublicReqCreateContactOptionsDTO`](#publicreqcreatecontactoptionsdto) | - |  |

### PublicReqCreateContactOptionsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `upsert` | boolean | - | Com esta opção habilitada, se o contato já existir na base de dados, ele será atualizado com os novos dados e retornado. |
| `upsertFields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Defina quais campos deverão ser motificados em caso de upsert (quando o contato já existe), se não for informado todos os campos serão afetados |
| `upsertTagOperation` | enum: `INSERTIFNOTEXISTS`, `DELETEIFEXISTS`, `REPLACEALL` | - | Defina como deve ser a alteração no campo Etiquetas em caso de upsert(quando o contato já existe) InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. (Opção padrão) |
| `getIfExists` | boolean | - | Com esta opção habilitada, se o contato já existir na base de dados, ele será retornado e nenhum dado será atualizado; |

### PublicReqFilterContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `pageNumber` | integer(int32) | - | Número da página a ser obtida. |
| `pageSize` | integer(int32) | - | Tamanho da página a ser obtida. |
| `orderBy` | string | - | Nome do campo para ser utilizado como pivô da ordenação. |
| `orderDirection` | enum: `ASCENDING`, `DESCENDING` | - | Determina se a ordenação deve ser crescente ou decrescente. |
| `createdAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `updatedAt` | [`PublicDateFilterDTO`](#publicdatefilterdto) | - |  |
| `includeDetails` | enum: `Tags`, `CustomFields`, `Portfolios`[] | - | Detalhes que devem ser incluídos na resposta. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status dos contatos a serem listados. Caso não informado, o valor padrão é ACTIVE. |
| `textFilter` | string | - | Filtro textual. A busca é realizada nos atributos textuais relevantes do contato. |
| `name` | string | - | Filtro por nome. |
| `phoneNumber` | string | - | Filtro por número de telefone. |
| `email` | string | - | Filtro por email. |
| `instagram` | string | - | Filtro por nome de usuário do Instagram. |
| `tagIds` | string(uuid)[] | - | Filtro por etiquetas usando IDs. |
| `tagNames` | string[] | - | Filtro por etiquetas usando nomes. |
| `portfolioIds` | string(uuid)[] | - | Filtro por carteiras usando IDs. |
| `portfolioNames` | string[] | - | Filtro por carteiras usando nomes. |
| `origin` | enum: `CREATED_BY_USER`, `CREATED_FROM_HUB`, `IMPORTED` | - | Filtro por origem. |
| `customFields` | object | - | Filtro por valores de campos personalizados. |
| `metadata` | object | - | Filtro por metadados. |

### PublicReqUpdateContactDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `PhoneNumber`, `Email`, `Instagram`, `Annotation`, `Tags`, `Status`, `CustomFields`, `PictureUrl`, `Portfolio`, `SequenceIds`, `Utm` … (+1)[] | - | Campos a serem atualizados. |
| `name` | string | - | Nome do contato. |
| `phoneNumber` | string | - | Número no WhatsApp. |
| `email` | string | - | Endereço de email. |
| `instagram` | string | - | Nome de usuário no Instagram. |
| `annotation` | string | - | Notas internas da equipe. |
| `tagIds` | string(uuid)[] | - | IDs das etiquetas atribuídas. |
| `tagNames` | string[] | - | Nomes das etiquetas atribuídas. Este campo será ignorado caso `TagIds` seja definido. |
| `portfolioIds` | string(uuid)[] | - | IDs das carteiras atribuídas. |
| `portfolioNames` | string[] | - | Nomes das carteiras atribuídas. Este campo será ignorado caso `PortfolioIds` seja definido. |
| `sequenceIds` | string(uuid)[] | - | IDs das sequências atribuídas. |
| `status` | enum: `ACTIVE`, `ARCHIVED`, `BLOCKED` | - | Status do contato. |
| `pictureUrl` | string | - | Informe neste campo uma Url para definição da imagem do contato |
| `customFields` | object | - | Objeto chave-valor para definir valores de campos personalizados no contato. Cada item do objeto deverá ter como nome a chave do campo personalizado. Caso a chave não corresponda a algum campo personalizado ou o tipo de dados do valor seja incompatível, o item será ignorado. |
| `metadata` | object | - | Metadados relevantes para o contato. Neste campo, pode ser salvo qualquer propriedade adicional para o contato, na estrutura chave-valor. - Para adicionar um metadado: utilize uma chave não utilizada anteriormente neste contato, atribuindo o novo valor; - Para atualizar um metadado: utilize a chave salva anteriormente neste contato, atribuindo o novo valor; - Para remover um metadado: utilize a chave salva anteriormente, atribuindo valor nulo. |
| `utm` | [`PublicUtmDTO`](#publicutmdto) | - |  |
| `options` | [`PublicReqContactUpdatePartialOptionsDTO`](#publicreqcontactupdatepartialoptionsdto) | - |  |

### PublicReqUpdateContactTagDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `tagNames` | string[] | - | Lista de nomes das etiquetas |
| `tagIds` | string(uuid)[] | - | Lista de identificadores das etiquetas (opcional se o nome for informado) |
| `operation` | enum: `InsertIfNotExists`, `DeleteIfExists`, `ReplaceAll` | - | Tipo de operação: InsertIfNotExists - Insere as etiquetas que já não estiverem relacionadas ao contato; DeleteIfExists - Remove as etiquetas que já estiverem relacionadas no contato; ReplaceAll - Remove todas as etiquetas do contato e inclui as que estão sendo informadas. |

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
