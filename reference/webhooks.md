# Webhooks

Serviço `core` — base `https://api.wts.chat/core`. Autenticação: `Authorization: Bearer <token>`.

## `GET` /core/v1/webhook/event — Listar eventos

Listagem dos eventos de webhook que podem ser assinados.

**Resposta 200** [`PublicWebhookEventDTO`](#publicwebhookeventdto)[]

Array de [`PublicWebhookEventDTO`](#publicwebhookeventdto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `event` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4) | - |  |
| `description` | string | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-event

## `GET` /core/v1/webhook/subscription — Listar assinaturas

Listagem das assinaturas de webhook ativas e inativas.

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)[]

Array de [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto).
| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-subscription

## `POST` /core/v1/webhook/subscription — Cria assinatura

Cria assinatura de webhook.

**Body** [`PublicReqCreateWebhookSubscriptionDTO`](#publicreqcreatewebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome para identificação da assinatura |
| `url` | string | sim | URL destino para onde serão enviadas requisições POST |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa) |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | sim | Eventos que deverão ser enviados para esta assinatura |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/post_v1-webhook-subscription

## `DELETE` /core/v1/webhook/subscription/{subscriptionId} — Remove assinatura

Remove assinatura de webhook.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Resposta 200** sem corpo.

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/delete_v1-webhook-subscription-subscriptionid

## `GET` /core/v1/webhook/subscription/{subscriptionId} — Busca assinatura por ID

Busca assinatura de webhook através do ID.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/get_v1-webhook-subscription-subscriptionid

## `PUT` /core/v1/webhook/subscription/{subscriptionId} — Atualiza assinatura

Atualiza assinatura de webhook.

**Parâmetros**

| Nome | Em | Obrig. | Tipo | Descrição |
|---|---|---|---|---|
| `subscriptionId` | path | sim | string(uuid) | ID da assinatura de webhook. |

**Body** [`PublicReqUpdateWebhookSubscriptionDTO`](#publicrequpdatewebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `Url`, `Events`, `Enabled`[] | sim | Campos a serem atualizados. |
| `name` | string | - | Nome para identificação da assinatura. |
| `url` | string | - | URL destino para onde serão enviadas requisições POST. |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa). |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | - | Tópicos de webhook que deverão ser inscritos nesta assinatura. |

**Resposta 200** [`PublicWebhookSubscriptionDTO`](#publicwebhooksubscriptiondto)

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |

Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  
Doc: https://flwchat.readme.io/reference/put_v1-webhook-subscription-subscriptionid

---

## Schemas

### PublicReqCreateWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `name` | string | sim | Nome para identificação da assinatura |
| `url` | string | sim | URL destino para onde serão enviadas requisições POST |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa) |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | sim | Eventos que deverão ser enviados para esta assinatura |

### PublicReqUpdateWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `fields` | enum: `Name`, `Url`, `Events`, `Enabled`[] | sim | Campos a serem atualizados. |
| `name` | string | - | Nome para identificação da assinatura. |
| `url` | string | - | URL destino para onde serão enviadas requisições POST. |
| `enabled` | boolean | - | Estado inicial da assinatura (ativa ou inativa). |
| `events` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4)[] | - | Tópicos de webhook que deverão ser inscritos nesta assinatura. |

### PublicWebhookEventDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `event` | enum: `SESSION_NEW`, `SESSION_UPDATE`, `SESSION_COMPLETE`, `MESSAGE_RECEIVED`, `MESSAGE_UPDATED`, `MESSAGE_SENT`, `CONTACT_NEW`, `CONTACT_UPDATE`, `CONTACT_TAG_UPDATE`, `PAYMENT_NEW`, `PAYMENT_UPDATE`, `PANEL_CARD_NEW` … (+4) | - |  |
| `description` | string | - |  |

### PublicWebhookSubscriptionDTO

| Campo | Tipo | Obrig. | Descrição |
|---|---|---|---|
| `id` | string(uuid) | - |  |
| `createdAt` | string(date-time) | - |  |
| `updatedAt` | string(date-time) | - |  |
| `companyId` | string(uuid) | - |  |
| `name` | string | - |  |
| `url` | string | - |  |
| `enabled` | boolean | - |  |
| `events` | [`PublicWebhookEventDTO`](#publicwebhookeventdto)[] | - |  |
