# Campos

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/custom-field — Listar

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `EntityType` | query | - | enum: `CONTACT`, `PANEL` | Tipo de entidade do campo personalizado. |
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
Doc: https://flwchat.readme.io/reference/get_v1-custom-field

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
