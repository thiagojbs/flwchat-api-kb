# Equipes

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `POST` /core/v1/department — Criar

**Body** [`PublicReqSaveDepartmentDTO`](#publicreqsavedepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `agents` | [`PublicDepartmentAgentCreateDTO`](#publicdepartmentagentcreatedto)[] | - | Lista de usuários para criar na equipe |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-department

## `DELETE` /core/v1/department/{id} — Excluir

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-department-id

## `GET` /core/v1/department/{id} — Obter por ID

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) |  |
| `includeDetails` | query | - | enum: `All`, `Agents`, `Channels` |  |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-department-id

## `PUT` /core/v1/department/{id} — Atualizar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe. |

**Body** [`PublicReqUpdateDepartmentDTO`](#publicrequpdatedepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `fields` | enum: `Name`, `Description`, `IsDefault`, `DistributionIsEnabled`, `ChannelsConfig`, `RestrictionType`, `DistributionConfig`[] | sim | Campos que devem ser atualizados |

**Resposta 200** [`PublicDepartmentDTO`](#publicdepartmentdto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-department-id

## `PUT` /core/v1/department/{id}/agents — Atualizar usuários

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe |

**Body** [`PublicReqUpdateDepartmentAgent`](#publicrequpdatedepartmentagent)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

**Resposta 200** [`PublicReqUpdateDepartmentAgent`](#publicrequpdatedepartmentagent)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-department-id-agents

## `GET` /core/v1/department/{id}/channel — Listar canais

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `id` | path | sim | string(uuid) | ID da equipe |

**Resposta 200** [`PublicDepartmentListChannelDTO`](#publicdepartmentlistchanneldto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - |  |
| `channels` | string(uuid)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-department-id-channel

## `GET` /core/v2/department — Listar

**Resposta 200** [`PublicDepartmentDTOV2`](#publicdepartmentdtov2)[]

Array de [`PublicDepartmentDTOV2`](#publicdepartmentdtov2).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v2-department

---

## Schemas

### DepartmentChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `number` | string | - |  |
| `name` | string | - |  |
| `type` | string | - |  |

### DepartmentDetailsDistributionConfigDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `expirationIsEnabled` | boolean | - |  |
| `maximumDurationInMinutes` | integer(int32) | - |  |
| `inactivityTimeInMinutes` | integer(int32) | - |  |

### PublicAgentUpdateDepartmentItemDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicDepartmentAgentCreateDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | sim | ID do usuário |
| `isAgent` | boolean | - | Se é atendente na equipe |
| `isSupervisor` | boolean | - | Se é supervisor na equipe |

### PublicDepartmentAgentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `userId` | string(uuid) | - |  |
| `departmentId` | string(uuid) | - |  |
| `isAgent` | boolean | - |  |
| `isSupervisor` | boolean | - |  |

### PublicDepartmentChannelsDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - | Escopo de canais permitidos |
| `channels` | string[] | - | ID, nome ou numero dos canais permitidos (quando escopo é SELECTED) |

### PublicDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |
| `description` | string | - |  |
| `isPrivate` | boolean | - |  |

### PublicDepartmentDTOV2

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `companyId` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `directLinks` | object | - |  |
| `updatedAt` | string(date-time) | - |  |
| `name` | string | - |  |
| `isDefault` | boolean | - |  |
| `distribuitionEnabled` | boolean | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - |  |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `agents` | [`PublicDepartmentAgentDTO`](#publicdepartmentagentdto)[] | - |  |
| `channels` | [`DepartmentChannelDTO`](#departmentchanneldto)[] | - |  |

### PublicDepartmentListChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `scope` | enum: `ALL`, `NONE`, `SELECTED` | - |  |
| `channels` | string(uuid)[] | - |  |

### PublicReqSaveDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `agents` | [`PublicDepartmentAgentCreateDTO`](#publicdepartmentagentcreatedto)[] | - | Lista de usuários para criar na equipe |

### PublicReqUpdateDepartmentAgent

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `action` | enum: `ReplaceAll`, `Upsert`, `Remove` | sim |  |
| `items` | [`PublicAgentUpdateDepartmentItemDTO`](#publicagentupdatedepartmentitemdto)[] | sim |  |

### PublicReqUpdateDepartmentDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | - | Nome da equipe |
| `isDefault` | boolean | - | Se é a equipe padrão |
| `distributionIsEnabled` | boolean | - | Se a distribuição está habilitada |
| `distributionConfig` | [`DepartmentDetailsDistributionConfigDTO`](#departmentdetailsdistributionconfigdto) | - |  |
| `restrictionType` | enum: `NONE`, `DEPARTMENT_RESTRICTION`, `USER_RESTRICTION` | - | Tipo de restrição |
| `channelsConfig` | [`PublicDepartmentChannelsDTO`](#publicdepartmentchannelsdto) | - |  |
| `fields` | enum: `Name`, `Description`, `IsDefault`, `DistributionIsEnabled`, `ChannelsConfig`, `RestrictionType`, `DistributionConfig`[] | sim | Campos que devem ser atualizados |
