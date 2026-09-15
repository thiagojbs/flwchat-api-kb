# Canais de Atendimento

Serviço `chat` — base `https://api.wts.chat/chat`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /chat/v1/channel — Listar

Listagem de canais de atendimento.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `ChannelType` | query | - | enum: `All`, `Whatsapp`, `Messenger`, `Instagram` | Tipo do canal. |

**Resposta 200** [`PublicChannelDTO`](#publicchanneldto)[]

Array de [`PublicChannelDTO`](#publicchanneldto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `type` | enum: `Dialog360_WhatsApp`, `CloudAPI_WhatsApp`, `ZAPI_WhatsApp`, `EvolutionApi_WhatsApp`, `Instagram`, `Messenger` | - |  |
| `number` | string | - |  |
| `numberFormatted` | string | - |  |
| `identity` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-channel

---

## Schemas

### PublicChannelDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `active` | boolean | - |  |
| `type` | enum: `Dialog360_WhatsApp`, `CloudAPI_WhatsApp`, `ZAPI_WhatsApp`, `EvolutionApi_WhatsApp`, `Instagram`, `Messenger` | - |  |
| `number` | string | - |  |
| `numberFormatted` | string | - |  |
| `identity` | [`PublicChannelIdentityDTO`](#publicchannelidentitydto) | - |  |

### PublicChannelIdentityDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `humanId` | string | - |  |
| `platform` | string | - |  |
| `provider` | string | - |  |
| `providerVariable` | string | - |  |
| `pictureUrl` | string | - |  |
| `displayName` | string | - |  |
