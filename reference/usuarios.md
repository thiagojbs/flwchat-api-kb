# Usuários

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/agent — Listar

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)[]

Array de [`PublicAgentDTO`](#publicagentdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-agent

## `POST` /core/v1/agent — Criar

**Body** [`PublicAgentCreateDTO`](#publicagentcreatedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome do usuário |
| `email` | string(email) | - | Email do usuário |
| `phoneNumber` | string | - | Telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | sim | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent

## `DELETE` /core/v1/agent/{id} — Excluir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`RequestAgentDepartmentDeleteDTO`](#requestagentdepartmentdeletedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionResolution` | enum: `COMPLETE`, `TRANSFER`, `RETURN_TO_PENDING` | - |  |
| `transferUserId` | string(uuid) | - | ID do usuário que receberá os atendimentos em andamento. Obrigatório quando o campo sessionResolution for igual a TRANSFER |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-agent-id

## `GET` /core/v1/agent/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-agent-id

## `PUT` /core/v1/agent/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentUpdatePartialDTO`](#publicagentupdatepartialdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do usuário |
| `shortName` | string | - | Nome curto/apelido do usuário |
| `email` | string | - | Email do usuário |
| `phoneNumber` | string | - | Número de telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | - | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |
| `fields` | enum: `Undefined`, `Name`, `ShortName`, `PhoneNumber`, `Email`, `Profile`, `Availability`[] | sim | Campos que devem ser atualizados |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-agent-id

## `POST` /core/v1/agent/{id}/departments — Atualizar equipes

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentDepartmentUpdateDTO`](#publicagentdepartmentupdatedto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim | Ação a ser executada: REPLACE_ALL, UPSERT ou REMOVE |
| `items` | [`PublicAgentDepartmentItemDTO`](#publicagentdepartmentitemdto)[] | sim | Lista de equipes para atualização |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-departments

## `POST` /core/v1/agent/{id}/logout — Fazer logout

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-logout

## `POST` /core/v1/agent/{id}/status — Alterar status

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID do usuário |

**Body** [`PublicAgentChangeStatusDTO`](#publicagentchangestatusdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `status` | enum: `Undefined`, `Active`, `Blocked` | sim | Novo status do usuário |

**Resposta 200** [`PublicAgentDTO`](#publicagentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-agent-id-status

---

## Schemas

### PublicAgentChangeStatusDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `status` | enum: `Undefined`, `Active`, `Blocked` | sim | Novo status do usuário |

### PublicAgentCreateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome do usuário |
| `email` | string(email) | - | Email do usuário |
| `phoneNumber` | string | - | Telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | sim | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |

### PublicAgentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `name` | string | - |  |
| `shortName` | string | - |  |
| `email` | string | - |  |
| `phoneNumber` | string | - |  |
| `phoneNumberFormatted` | string | - |  |
| `profile` | string | - |  |
| `isOwner` | boolean | - |  |
| `departments` | [`PublicAgentDepartmentDTO`](#publicagentdepartmentdto)[] | - |  |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Enum que representa o status de disponibilidade de um usuário |

### PublicAgentDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `agentId` | string(uuid) | - |  |
| `userId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicAgentDepartmentItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `departmentId` | string | sim | ID da equipe |
| `isAgent` | boolean | - | Se é usuário na equipe |
| `isSupervisor` | boolean | - | Se é supervisor na equipe |

### PublicAgentDepartmentUpdateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim | Ação a ser executada: REPLACE_ALL, UPSERT ou REMOVE |
| `items` | [`PublicAgentDepartmentItemDTO`](#publicagentdepartmentitemdto)[] | sim | Lista de equipes para atualização |

### PublicAgentUpdatePartialDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome do usuário |
| `shortName` | string | - | Nome curto/apelido do usuário |
| `email` | string | - | Email do usuário |
| `phoneNumber` | string | - | Número de telefone do usuário |
| `profile` | enum: `Admin`, `Agent`, `RestrictedAgent` | - | Perfil do usuário |
| `availability` | enum: `AVAILABLE`, `UNAVAILABLE` | - | Disponibilidade do usuário |
| `fields` | enum: `Undefined`, `Name`, `ShortName`, `PhoneNumber`, `Email`, `Profile`, `Availability`[] | sim | Campos que devem ser atualizados |

### RequestAgentDepartmentDeleteDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `sessionResolution` | enum: `COMPLETE`, `TRANSFER`, `RETURN_TO_PENDING` | - |  |
| `transferUserId` | string(uuid) | - | ID do usuário que receberá os atendimentos em andamento. Obrigatório quando o campo sessionResolution for igual a TRANSFER |
